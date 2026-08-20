#!/usr/bin/env python3
"""Pull the strongest still frames out of a video, favouring people.

Three passes: find the cuts; score cheap downscaled candidates inside each
shot; then re-sample a short window around each winner at the native frame
rate, so a blink or a mid-word mouth shape can be stepped over rather than
being whatever the coarse sampling happened to land on.

Frames keep the source aspect ratio. The only geometry change is trimming
black padding (letterbox/pillarbox), which screen-recorded sources carry.

    python3 tools/cinematic_frames.py video.mp4 -o stills -n 24
"""

import argparse
import json
import re
import shutil
import subprocess
import sys
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw, ImageFont

try:
    import cv2
except ImportError:
    cv2 = None

# Picture-quality weights, summing to 0.70; faces and their penalties own the
# rest. Sharpness leads because a motion-blurred frame is unusable no matter
# how good the colour is.
W_SHARP, W_CONTRAST, W_COLOR, W_CLIP = 0.24, 0.11, 0.11, 0.09
W_FACE = 0.25           # bonus for a person being present and large enough
W_COMP = 0.20           # bonus for the frame being deliberately composed
P_BLINK = 0.30          # penalty for eyes reading as shut
P_MOUTH = 0.15          # penalty for a wide-open mouth
P_EDGE = 0.12           # penalty for a face clipped by the frame border

# Rule-of-thirds intersections in normalised coordinates.
THIRDS = [(1 / 3, 1 / 3), (2 / 3, 1 / 3), (1 / 3, 2 / 3), (2 / 3, 2 / 3)]

DEFAULT_MODEL = Path(__file__).parent / "models" / "face_detection_yunet_2023mar.onnx"
COARSE_WIDTH = 640      # faces need pixels; 320 is too small to detect on


def ffmpeg_bin() -> str:
    exe = shutil.which("ffmpeg")
    if exe:
        return exe
    import imageio_ffmpeg

    return imageio_ffmpeg.get_ffmpeg_exe()


def ffprobe_bin() -> str:
    return shutil.which("ffprobe") or ""


def probe(video: Path) -> dict:
    """Width, height, duration and frame rate of the first video stream."""
    probe_exe = ffprobe_bin()
    if probe_exe:
        out = subprocess.run(
            [probe_exe, "-v", "error", "-select_streams", "v:0", "-show_streams",
             "-show_format", "-of", "json", str(video)],
            capture_output=True, text=True, check=True,
        ).stdout
        data = json.loads(out)
        st = data["streams"][0]
        num, den = (st.get("r_frame_rate") or "24/1").split("/")
        return {
            "width": int(st["width"]),
            "height": int(st["height"]),
            "fps": float(num) / float(den or 1),
            "duration": float(st.get("duration") or data["format"]["duration"]),
        }

    err = subprocess.run(
        [ffmpeg_bin(), "-i", str(video), "-f", "null", "-"],
        capture_output=True, text=True,
    ).stderr
    dim = re.search(r"(\d{2,5})x(\d{2,5})", err)
    fps = re.search(r"([\d.]+) fps", err)
    dur = re.search(r"Duration: (\d+):(\d+):([\d.]+)", err)
    if not (dim and dur):
        raise RuntimeError(f"could not probe {video}")
    h, m, s = dur.groups()
    return {
        "width": int(dim.group(1)),
        "height": int(dim.group(2)),
        "fps": float(fps.group(1)) if fps else 24.0,
        "duration": int(h) * 3600 + int(m) * 60 + float(s),
    }


def detect_cuts(video: Path, threshold: float) -> list[float]:
    """Timestamps where the picture changes hard enough to call it a new shot."""
    proc = subprocess.run(
        [ffmpeg_bin(), "-v", "info", "-i", str(video),
         "-vf", f"select='gt(scene,{threshold})',metadata=print:file=-",
         "-an", "-f", "null", "-"],
        capture_output=True, text=True,
    )
    return sorted({round(float(m), 3)
                   for m in re.findall(r"pts_time:([\d.]+)", proc.stdout)})


def detect_letterbox(video: Path, meta: dict, samples: int = 6):
    """Union of ffmpeg's cropdetect guesses, so we never cut into real picture.

    Screen recordings arrive padded: a 2.39:1 cut played full-screen on a phone
    sits in a box of black. Scoring goes wrong if we keep it, and it is the one
    thing we are willing to crop.
    """
    boxes = []
    step = max(meta["duration"] / (samples + 1), 0.5)
    for i in range(1, samples + 1):
        err = subprocess.run(
            [ffmpeg_bin(), "-v", "info", "-ss", f"{step * i:.2f}", "-i", str(video),
             "-vf", "cropdetect=24:2:0", "-frames:v", "40", "-an", "-f", "null", "-"],
            capture_output=True, text=True,
        ).stderr
        for w, h, x, y in re.findall(r"crop=(\d+):(\d+):(\d+):(\d+)", err):
            w, h, x, y = int(w), int(h), int(x), int(y)
            if w > 0 and h > 0:
                boxes.append((x, y, x + w, y + h))
    if not boxes:
        return None

    left = min(b[0] for b in boxes)
    top = min(b[1] for b in boxes)
    right = max(b[2] for b in boxes)
    bottom = max(b[3] for b in boxes)
    w = min(right - left, meta["width"] - left) // 2 * 2
    h = min(bottom - top, meta["height"] - top) // 2 * 2
    if w < 16 or h < 16:
        return None
    if w >= meta["width"] * 0.98 and h >= meta["height"] * 0.98:
        return None
    return {"w": w, "h": h, "x": left, "y": top,
            "filter": f"crop={w}:{h}:{left}:{top}"}


def stream_frames(video: Path, width: int, height: int, crop: str | None = None,
                  rate: float | None = None, start: float | None = None,
                  duration: float | None = None):
    """Decode to raw RGB and yield (index, array). Small and fast by design."""
    cmd = [ffmpeg_bin(), "-v", "error"]
    if start is not None:
        cmd += ["-ss", f"{max(start, 0):.3f}"]
    cmd += ["-i", str(video)]
    if duration is not None:
        cmd += ["-t", f"{duration:.3f}"]
    chain = []
    if crop:
        chain.append(crop)
    if rate:
        chain.append(f"fps={rate}")
    chain.append(f"scale={width}:{height}")
    cmd += ["-vf", ",".join(chain), "-f", "rawvideo", "-pix_fmt", "rgb24", "-"]

    frame_bytes = width * height * 3
    proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.DEVNULL)
    idx = 0
    try:
        while True:
            buf = proc.stdout.read(frame_bytes)
            if len(buf) < frame_bytes:
                break
            yield idx, np.frombuffer(buf, np.uint8).reshape(height, width, 3)
            idx += 1
    finally:
        proc.stdout.close()
        proc.wait()


def luma_of(rgb: np.ndarray) -> np.ndarray:
    f = rgb.astype(np.float32)
    return 0.2126 * f[..., 0] + 0.7152 * f[..., 1] + 0.0722 * f[..., 2]


def laplacian(luma: np.ndarray) -> np.ndarray:
    """Second derivative — high where edges are crisp, flat under motion blur."""
    return (4 * luma[1:-1, 1:-1] - luma[:-2, 1:-1] - luma[2:, 1:-1]
            - luma[1:-1, :-2] - luma[1:-1, 2:])


def measure(rgb: np.ndarray, luma: np.ndarray | None = None) -> dict:
    """Cheap proxies for 'does this hold up as a still'."""
    f = rgb.astype(np.float32)
    r, g, b = f[..., 0], f[..., 1], f[..., 2]
    if luma is None:
        luma = luma_of(rgb)
    lap = laplacian(luma)

    # Hasler-Susstrunk colourfulness.
    rg, yb = r - g, 0.5 * (r + g) - b
    return {
        "sharpness": float(lap.var()),
        "contrast": float(luma.std()),
        "color": float(np.hypot(rg.std(), yb.std())
                       + 0.3 * np.hypot(rg.mean(), yb.mean())),
        "clipped": float((luma < 6).mean() + (luma > 249).mean()),
        "brightness": float(luma.mean()),
    }


def _patch(luma: np.ndarray, cx: float, cy: float, w: float, h: float):
    x0, x1 = int(round(cx - w / 2)), int(round(cx + w / 2))
    y0, y1 = int(round(cy - h / 2)), int(round(cy + h / 2))
    x0, y0 = max(x0, 0), max(y0, 0)
    x1, y1 = min(x1, luma.shape[1]), min(y1, luma.shape[0])
    if x1 - x0 < 3 or y1 - y0 < 3:
        return None
    return luma[y0:y1, x0:x1]


def eye_openness(luma: np.ndarray, eye_xy, iod: float, face_std: float) -> float | None:
    """Rough 0..1 openness from local detail around an eye landmark.

    An open eye puts a dark iris against bright sclera inside a small box, so
    the patch carries far more local variation than the closed lid does. This
    is a proxy, not a landmark model — it ranks frames within a shot well
    enough to step off a blink, which is all it is asked to do.
    """
    patch = _patch(luma, eye_xy[0], eye_xy[1], iod * 0.42, iod * 0.26)
    if patch is None or face_std < 1e-3:
        return None
    detail = patch.std() / face_std
    gy = np.abs(np.diff(patch, axis=0)).mean() / (face_std + 1e-6)
    raw = 0.6 * detail + 0.4 * gy
    return float(np.clip((raw - 0.32) / 0.5, 0.0, 1.0))


def mouth_openness(luma: np.ndarray, m_right, m_left, face_med: float) -> float | None:
    """Fraction of the mouth box reading as cavity — dark relative to the face."""
    cx = (m_right[0] + m_left[0]) / 2
    cy = (m_right[1] + m_left[1]) / 2
    width = float(np.hypot(m_left[0] - m_right[0], m_left[1] - m_right[1]))
    if width < 4:
        return None
    patch = _patch(luma, cx, cy + width * 0.12, width * 1.05, width * 0.85)
    if patch is None:
        return None
    dark = float((patch < face_med * 0.52).mean())
    return float(np.clip((dark - 0.12) / 0.4, 0.0, 1.0))


def subject_center(luma: np.ndarray, boxes) -> tuple[float, float]:
    """Where the eye lands: the faces if we have them, else where the detail is."""
    h, w = luma.shape
    if boxes:
        total = sum(b[2] * b[3] for b in boxes) or 1.0
        cx = sum((b[0] + b[2] / 2) * b[2] * b[3] for b in boxes) / total
        cy = sum((b[1] + b[3] / 2) * b[2] * b[3] for b in boxes) / total
        return float(cx / w), float(cy / h)

    energy = np.abs(np.diff(luma, axis=1))[:-1, :] + np.abs(np.diff(luma, axis=0))[:, :-1]
    total = float(energy.sum())
    if total < 1e-6:
        return 0.5, 0.5
    ys, xs = np.indices(energy.shape)
    return (float((xs * energy).sum() / total) / energy.shape[1],
            float((ys * energy).sum() / total) / energy.shape[0])


def thirds_score(cx: float, cy: float) -> float:
    nearest = min(float(np.hypot(cx - px, cy - py)) for px, py in THIRDS)
    return float(np.clip(1.0 - nearest / 0.20, 0.0, 1.0))


def symmetry_score(luma: np.ndarray) -> float:
    """How well the frame mirrors about its vertical axis.

    Resample rather than stride: striding picks columns 0, 10, 20 ... whose
    mirrors land between samples, so the halves never line up and the measure
    collapses into one of smoothness instead of symmetry.

    The difference is normalised by the frame's own contrast, so a flat or
    defocused frame cannot score well just by having little to disagree about.
    """
    if luma.shape[0] < 16 or luma.shape[1] < 16:
        return 0.0
    small = cv2.resize(luma, (128, 72), interpolation=cv2.INTER_AREA) \
        if cv2 is not None else luma
    spread = float(small.std())
    if spread < 3.0:            # nothing to be symmetrical about
        return 0.0
    half = small.shape[1] // 2
    diff = float(np.abs(small[:, :half] - np.fliplr(small[:, half:half * 2])).mean())
    return float(np.clip(1.0 - diff / spread, 0.0, 1.0))


def separation(luma: np.ndarray, box) -> float:
    """Subject sharp against a soft background — the shallow-depth-of-field look."""
    h, w = luma.shape
    x0, y0 = max(int(box[0]), 0), max(int(box[1]), 0)
    x1 = min(int(box[0] + box[2]), w)
    y1 = min(int(box[1] + box[3]), h)
    if x1 - x0 < 8 or y1 - y0 < 8 or h < 8 or w < 8:
        return 0.5
    lap2 = laplacian(luma) ** 2           # indices are offset by one
    ix0, iy0 = max(x0 - 1, 0), max(y0 - 1, 0)
    ix1, iy1 = min(x1 - 1, lap2.shape[1]), min(y1 - 1, lap2.shape[0])
    if ix1 - ix0 < 2 or iy1 - iy0 < 2:
        return 0.5
    inside = lap2[iy0:iy1, ix0:ix1]
    in_sum, in_n = float(inside.sum()), inside.size
    bg_n = lap2.size - in_n
    if bg_n < 16:
        return 0.5
    bg_mean = (float(lap2.sum()) - in_sum) / bg_n
    ratio = (in_sum / in_n) / (bg_mean + 1e-6)
    return float(np.clip(0.5 + np.log10(ratio + 1e-9) / 2.0, 0.0, 1.0))


def composition(luma: np.ndarray, face_info: dict) -> dict:
    """Blend of framing cues. All proxies — they rank frames, they don't judge.

    Thirds and symmetry are taken as alternatives rather than added: a centred
    symmetrical frame and a subject on a third are both deliberate, and it is
    the unmotivated drift between them that reads as a grab.
    """
    h, w = luma.shape
    boxes = face_info.get("boxes") or []
    cx, cy = subject_center(luma, boxes)
    thirds = thirds_score(cx, cy)
    symmetry = symmetry_score(luma)
    placement = max(thirds, symmetry)

    edge, headroom, sep = 0.0, 1.0, 0.5
    if boxes:
        bx, by, bw, bh = max(boxes, key=lambda b: b[2] * b[3])
        area = max(bw * bh, 1e-6)
        spill = (max(-bx, 0) + max((bx + bw) - w, 0)) * bh \
            + (max(-by, 0) + max((by + bh) - h, 0)) * bw
        margin = 0.02 * min(w, h)
        gap = min(bx, by, w - (bx + bw), h - (by + bh))
        edge = float(np.clip(max(spill / area, (margin - gap) / margin), 0.0, 1.0))

        # Faces sit naturally a little above centre; the floor of the frame reads badly.
        headroom = float(np.clip(1.0 - abs((by + bh / 2) / h - 0.38) / 0.42, 0.0, 1.0))
        if by / h < 0.02:
            headroom *= 0.5
        sep = separation(luma, (bx, by, bw, bh))
        score = 0.45 * placement + 0.25 * headroom + 0.30 * sep
    else:
        score = 0.70 * placement + 0.30 * 0.5

    return {"placement": placement, "thirds": thirds, "symmetry": symmetry,
            "headroom": headroom, "separation": sep, "edge": edge,
            "composition": float(np.clip(score, 0.0, 1.0))}


class FaceScorer:
    """YuNet detection plus landmark-patch heuristics for eyes and mouth."""

    def __init__(self, model: Path, width: int, height: int, conf: float = 0.7):
        self.det = cv2.FaceDetectorYN.create(str(model), "", (width, height),
                                             conf, 0.3, 5000)
        self.area = float(width * height)

    def score(self, rgb: np.ndarray, luma: np.ndarray | None = None) -> dict:
        bgr = np.ascontiguousarray(rgb[..., ::-1])
        _, faces = self.det.detect(bgr)
        if faces is None or len(faces) == 0:
            return {"faces": 0, "face_frac": 0.0, "presence": 0.0,
                    "blink": 0.0, "mouth": 0.0, "boxes": []}

        if luma is None:
            luma = luma_of(rgb)

        # Judge eyes and mouth on the biggest face; that is the one a viewer reads.
        biggest = max(faces, key=lambda r: r[2] * r[3])
        x, y, w, h = (float(v) for v in biggest[:4])
        pts = [(float(biggest[4 + 2 * i]), float(biggest[5 + 2 * i]))
               for i in range(5)]
        r_eye, l_eye, _nose, r_mouth, l_mouth = pts

        face_frac = float(sum(r[2] * r[3] for r in faces) / self.area)
        # sqrt so a distant figure still registers without a close-up dominating.
        presence = float(np.clip(np.sqrt(max(w * h, 0.0) / self.area) / 0.32, 0, 1))

        # Reference contrast and skin tone come from the brow/eye band only.
        # Measuring across the whole face couples the two signals: a wide-open
        # mouth is a big dark blob that inflates face-wide contrast and makes
        # open eyes read as shut.
        upper = _patch(luma, x + w / 2, y + h * 0.32, w, h * 0.55)
        face_std = float(upper.std()) if upper is not None else 0.0
        face_med = float(np.median(upper)) if upper is not None else 128.0

        iod = float(np.hypot(l_eye[0] - r_eye[0], l_eye[1] - r_eye[1]))
        blink = 0.0
        if iod >= 10:   # below this the eye box is a handful of pixels — no call
            opens = [o for o in (eye_openness(luma, r_eye, iod, face_std),
                                 eye_openness(luma, l_eye, iod, face_std))
                     if o is not None]
            if opens:
                blink = float(1.0 - max(opens))

        mouth = mouth_openness(luma, r_mouth, l_mouth, face_med) or 0.0
        return {"faces": int(len(faces)), "face_frac": face_frac,
                "presence": presence, "blink": blink, "mouth": float(mouth),
                "boxes": [tuple(float(v) for v in r[:4]) for r in faces]}


def rank(values: np.ndarray) -> np.ndarray:
    """Percentile rank in 0..1, so unlike units can be blended."""
    if len(values) < 2 or np.ptp(values) == 0:
        return np.full(len(values), 0.5)
    return values.argsort().argsort().astype(np.float64) / (len(values) - 1)


def blend(metrics: list[dict], faces: list[dict] | None,
          comps: list[dict] | None = None) -> np.ndarray:
    """Quality and composition ranks, plus faces, minus the penalties."""
    def col(name):
        return np.array([m[name] for m in metrics], dtype=np.float64)

    score = (W_SHARP * rank(col("sharpness"))
             + W_CONTRAST * rank(col("contrast"))
             + W_COLOR * rank(col("color"))
             + W_CLIP * (1.0 - rank(col("clipped"))))
    if faces:
        score = (score
                 + W_FACE * np.array([f["presence"] for f in faces])
                 - P_BLINK * np.array([f["blink"] for f in faces])
                 - P_MOUTH * np.array([f["mouth"] for f in faces])
                 - P_EDGE * np.array([c["edge"] for c in comps] if comps
                                     else [0.0] * len(faces)))
    if comps:
        score = score + W_COMP * np.array([c["composition"] for c in comps])
    return score


def analyse(rgb: np.ndarray, scorer, want_comp: bool):
    """One decode, one luma, all three scorers."""
    luma = luma_of(rgb)
    face = scorer.score(rgb, luma) if scorer else None
    comp = composition(luma, face or {}) if want_comp else None
    return measure(rgb, luma), face, comp


def shot_index(ts: float, cuts: list[float]) -> int:
    lo, hi = 0, len(cuts)
    while lo < hi:
        mid = (lo + hi) // 2
        if cuts[mid] <= ts:
            lo = mid + 1
        else:
            hi = mid
    return lo


def extract_full(video: Path, ts: float, dest: Path, crop: str | None = None):
    cmd = [ffmpeg_bin(), "-v", "error", "-y", "-ss", f"{ts:.3f}", "-i", str(video)]
    if crop:
        cmd += ["-vf", crop]
    cmd += ["-frames:v", "1", "-pix_fmt", "rgb24", str(dest)]
    subprocess.run(cmd, check=True, capture_output=True)


def timecode(ts: float) -> str:
    return f"{int(ts // 60):d}:{ts % 60:05.2f}"


def contact_sheet(picks: list[dict], out: Path, cols: int = 4, cell: int = 480):
    if not picks:
        return
    rows = (len(picks) + cols - 1) // cols
    label_h = 26
    thumbs = []
    for p in picks:
        im = Image.open(p["path"]).convert("RGB")
        im.thumbnail((cell, cell), Image.LANCZOS)
        thumbs.append(im)
    cw = max(t.width for t in thumbs)
    ch = max(t.height for t in thumbs) + label_h
    sheet = Image.new("RGB", (cw * cols, ch * rows), (16, 16, 16))
    draw = ImageDraw.Draw(sheet)
    try:
        font = ImageFont.truetype(
            "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 16)
    except OSError:
        font = ImageFont.load_default()
    for i, (thumb, p) in enumerate(zip(thumbs, picks)):
        x, y = (i % cols) * cw, (i // cols) * ch
        sheet.paste(thumb, (x + (cw - thumb.width) // 2, y))
        tag = f'#{p["n"]:02d}  {timecode(p["ts"])}'
        if p.get("faces"):
            tag += f'  {p["faces"]} face' + ("s" if p["faces"] > 1 else "")
        draw.text((x + 6, y + thumb.height + 4), tag, (235, 235, 235), font=font)
    sheet.save(out, quality=92)


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("video", type=Path)
    ap.add_argument("-o", "--outdir", type=Path, default=Path("stills"))
    ap.add_argument("-n", "--count", type=int, default=24)
    ap.add_argument("--rate", type=float, default=2.0,
                    help="candidate frames sampled per second (default 2)")
    ap.add_argument("--scene", type=float, default=0.25,
                    help="cut-detection sensitivity, 0-1 (default 0.25)")
    ap.add_argument("--min-gap", type=float, default=1.0,
                    help="minimum seconds between two keepers (default 1.0)")
    ap.add_argument("--refine-window", type=float, default=0.4,
                    help="seconds either side to step off a blink (default 0.4)")
    ap.add_argument("--faces-only", action="store_true",
                    help="discard shots with nobody in them")
    ap.add_argument("--no-faces", action="store_true",
                    help="skip face scoring entirely")
    ap.add_argument("--no-composition", action="store_true",
                    help="skip composition scoring entirely")
    ap.add_argument("--face-model", type=Path, default=DEFAULT_MODEL)
    ap.add_argument("--no-autocrop", action="store_true",
                    help="keep letterbox bars instead of trimming them")
    args = ap.parse_args()

    if not args.video.exists():
        print(f"no such file: {args.video}", file=sys.stderr)
        return 1

    meta = probe(args.video)
    print(f"{args.video.name}: {meta['width']}x{meta['height']} "
          f"{meta['fps']:.2f}fps {meta['duration']:.1f}s")

    box = None if args.no_autocrop else detect_letterbox(args.video, meta)
    crop = box["filter"] if box else None
    if box:
        print(f"trimming padding -> {box['w']}x{box['h']} (+{box['x']},{box['y']})")

    eff_w = box["w"] if box else meta["width"]
    eff_h = box["h"] if box else meta["height"]
    sw = COARSE_WIDTH
    sh = max(2, round(sw * eff_h / eff_w) // 2 * 2)

    scorer = None
    if not args.no_faces:
        if cv2 is None:
            print("opencv not installed — scoring without faces", file=sys.stderr)
        elif not args.face_model.exists():
            print(f"no face model at {args.face_model} — scoring without faces",
                  file=sys.stderr)
        else:
            scorer = FaceScorer(args.face_model, sw, sh)

    cuts = detect_cuts(args.video, args.scene)
    print(f"detected {len(cuts)} cuts -> {len(cuts) + 1} shots")

    want_comp = not args.no_composition
    stamps, metrics, faces, comps = [], [], [], []
    for idx, frame in stream_frames(args.video, sw, sh, crop, rate=args.rate):
        m, f, c = analyse(frame, scorer, want_comp)
        stamps.append(idx / args.rate)
        metrics.append(m)
        if scorer:
            faces.append(f)
        if want_comp:
            comps.append(c)
    if not stamps:
        print("decoded no frames — is this really a video file?", file=sys.stderr)
        return 1
    with_faces = sum(1 for f in faces if f["faces"]) if scorer else 0
    print(f"scored {len(stamps)} candidates"
          + (f", {with_faces} with faces" if scorer else ""))

    keep = [i for i, m in enumerate(metrics) if m["brightness"] > 12]
    if args.faces_only and scorer:
        only = [i for i in keep if faces[i]["faces"]]
        if only:
            keep = only
        else:
            print("no faces found anywhere — keeping all shots", file=sys.stderr)
    if not keep:
        keep = list(range(len(metrics)))

    score = blend([metrics[i] for i in keep],
                  [faces[i] for i in keep] if scorer else None,
                  [comps[i] for i in keep] if want_comp else None)

    # Best frame per shot, so we get coverage instead of ten stills of one setup.
    best: dict[int, tuple[float, float]] = {}
    for pos, i in enumerate(keep):
        shot = shot_index(stamps[i], cuts)
        if shot not in best or score[pos] > best[shot][1]:
            best[shot] = (stamps[i], float(score[pos]))

    chosen: list[tuple[float, float]] = []
    for ts, sc in sorted(best.values(), key=lambda t: -t[1]):
        if len(chosen) >= args.count:
            break
        if all(abs(ts - t) >= args.min_gap for t, _ in chosen):
            chosen.append((ts, sc))
    chosen.sort(key=lambda t: t[0])

    # Refinement: re-sample each winner's neighbourhood at the native frame
    # rate. A blink lasts a few frames, so the coarse 2fps grid can easily land
    # on one; here we get to step off it.
    refined = []
    win = args.refine_window
    for ts, sc in chosen:
        if win <= 0:
            refined.append({"ts": ts, "score": sc})
            continue
        start = max(ts - win, 0.0)
        local_ts, local_m, local_f, local_c = [], [], [], []
        for idx, frame in stream_frames(args.video, sw, sh, crop,
                                        start=start, duration=win * 2):
            m, f, c = analyse(frame, scorer, want_comp)
            local_ts.append(start + idx / meta["fps"])
            local_m.append(m)
            if scorer:
                local_f.append(f)
            if want_comp:
                local_c.append(c)
        if not local_ts:
            refined.append({"ts": ts, "score": sc})
            continue
        local_score = blend(local_m, local_f if scorer else None,
                            local_c if want_comp else None)
        j = int(np.argmax(local_score))
        entry = {"ts": local_ts[j], "score": float(local_score[j]),
                 "moved": round(local_ts[j] - ts, 3)}
        if scorer:
            entry.update(faces=local_f[j]["faces"],
                         blink=round(local_f[j]["blink"], 3),
                         mouth=round(local_f[j]["mouth"], 3))
        if want_comp:
            entry.update(composition=round(local_c[j]["composition"], 3),
                         thirds=round(local_c[j]["thirds"], 3),
                         symmetry=round(local_c[j]["symmetry"], 3),
                         headroom=round(local_c[j]["headroom"], 3),
                         separation=round(local_c[j]["separation"], 3),
                         edge=round(local_c[j]["edge"], 3))
        refined.append(entry)

    args.outdir.mkdir(parents=True, exist_ok=True)
    full_dir = args.outdir / "full"
    full_dir.mkdir(exist_ok=True)

    picks = []
    for n, r in enumerate(refined, 1):
        dest = full_dir / f"{n:02d}_{timecode(r['ts']).replace(':', 'm')}.png"
        extract_full(args.video, r["ts"], dest, crop)
        p = {"n": n, "path": dest, **r}
        picks.append(p)
        note = ""
        if scorer:
            note = f'  faces {r.get("faces", 0)}'
            if r.get("blink", 0) > 0.5:
                note += " (eyes uncertain)"
            if r.get("mouth", 0) > 0.6:
                note += " (mouth wide)"
        if want_comp:
            note += f'  comp {r.get("composition", 0):.2f}'
            if r.get("edge", 0) > 0.5:
                note += " (face at edge)"
        if r.get("moved"):
            note += f'  nudged {r["moved"]:+.2f}s'
        print(f'  #{n:02d}  {timecode(r["ts"])}  score {r["score"]:.3f}{note}')

    contact = args.outdir / "contact_sheet.jpg"
    contact_sheet(picks, contact)
    (args.outdir / "picks.json").write_text(json.dumps(
        [{k: (str(v) if isinstance(v, Path) else v) for k, v in p.items()}
         for p in picks], indent=2))
    print(f"\n{len(picks)} stills at native aspect in {args.outdir}"
          f"\ncontact sheet: {contact}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
