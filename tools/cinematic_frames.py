#!/usr/bin/env python3
"""Pull the strongest still frames out of a video.

Two passes: find the cuts, score cheap downscaled candidates inside each shot,
then re-extract only the winners at full resolution.

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

# Weights for the final blend. Sharpness leads because a motion-blurred frame is
# unusable no matter how nice the colour is.
W_SHARP, W_CONTRAST, W_COLOR, W_CLIP = 0.40, 0.22, 0.20, 0.18

CROPS = {"4x5": (4, 5), "9x16": (9, 16), "1x1": (1, 1)}


def ffmpeg_bin() -> str:
    exe = shutil.which("ffmpeg")
    if exe:
        return exe
    import imageio_ffmpeg

    return imageio_ffmpeg.get_ffmpeg_exe()


def ffprobe_bin() -> str:
    exe = shutil.which("ffprobe")
    if exe:
        return exe
    # imageio's ffmpeg build answers -show_streams too via the ffprobe sibling;
    # fall back to parsing ffmpeg output if no ffprobe exists.
    return ""


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

    # No ffprobe: read what ffmpeg prints to stderr on a null decode.
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
    sits in a box of black. Scoring and cropping both go wrong if we keep it.
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
    # Within a couple percent of the full frame means there was no padding.
    if w >= meta["width"] * 0.98 and h >= meta["height"] * 0.98:
        return None
    return {"w": w, "h": h, "x": left, "y": top,
            "filter": f"crop={w}:{h}:{left}:{top}"}


def sample_candidates(video: Path, rate: float, width: int, height: int,
                      crop: str | None = None):
    """Decode the whole video small and fast; yield (timestamp, RGB array)."""
    chain = f"fps={rate},scale={width}:{height}"
    if crop:
        chain = f"{crop},{chain}"
    cmd = [ffmpeg_bin(), "-v", "error", "-i", str(video),
           "-vf", chain,
           "-f", "rawvideo", "-pix_fmt", "rgb24", "-"]
    frame_bytes = width * height * 3
    proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.DEVNULL)
    idx = 0
    try:
        while True:
            buf = proc.stdout.read(frame_bytes)
            if len(buf) < frame_bytes:
                break
            arr = np.frombuffer(buf, np.uint8).reshape(height, width, 3)
            yield idx / rate, arr
            idx += 1
    finally:
        proc.stdout.close()
        proc.wait()


def measure(rgb: np.ndarray) -> dict:
    """Four cheap proxies for 'does this hold up as a still'."""
    f = rgb.astype(np.float32)
    r, g, b = f[..., 0], f[..., 1], f[..., 2]
    luma = 0.2126 * r + 0.7152 * g + 0.0722 * b

    # Laplacian energy — high when edges are crisp, near zero on motion blur.
    lap = (4 * luma[1:-1, 1:-1] - luma[:-2, 1:-1] - luma[2:, 1:-1]
           - luma[1:-1, :-2] - luma[1:-1, 2:])
    sharpness = float(lap.var())

    # Hasler-Susstrunk colourfulness.
    rg, yb = r - g, 0.5 * (r + g) - b
    color = float(np.hypot(rg.std(), yb.std())
                  + 0.3 * np.hypot(rg.mean(), yb.mean()))

    clipped = float((luma < 6).mean() + (luma > 249).mean())
    return {
        "sharpness": sharpness,
        "contrast": float(luma.std()),
        "color": color,
        "clipped": clipped,
        "brightness": float(luma.mean()),
    }


def rank(values: np.ndarray) -> np.ndarray:
    """Percentile rank in 0..1, so unlike units can be blended."""
    if len(values) < 2 or np.ptp(values) == 0:
        return np.full(len(values), 0.5)
    order = values.argsort().argsort().astype(np.float64)
    return order / (len(values) - 1)


def shot_index(ts: float, cuts: list[float]) -> int:
    lo, hi = 0, len(cuts)
    while lo < hi:
        mid = (lo + hi) // 2
        if cuts[mid] <= ts:
            lo = mid + 1
        else:
            hi = mid
    return lo


def extract_full(video: Path, ts: float, dest: Path,
                 crop: str | None = None) -> None:
    cmd = [ffmpeg_bin(), "-v", "error", "-y", "-ss", f"{ts:.3f}", "-i", str(video)]
    if crop:
        cmd += ["-vf", crop]
    cmd += ["-frames:v", "1", "-pix_fmt", "rgb24", str(dest)]
    subprocess.run(cmd, check=True, capture_output=True)


def center_crop(img: Image.Image, ratio: tuple[int, int]) -> Image.Image:
    want = ratio[0] / ratio[1]
    w, h = img.size
    if w / h > want:
        new_w = round(h * want)
        box = ((w - new_w) // 2, 0, (w - new_w) // 2 + new_w, h)
    else:
        new_h = round(w / want)
        box = (0, (h - new_h) // 2, w, (h - new_h) // 2 + new_h)
    return img.crop(box)


def timecode(ts: float) -> str:
    return f"{int(ts // 60):d}:{ts % 60:05.2f}"


def contact_sheet(picks: list[dict], out: Path, cols: int = 4, cell: int = 480):
    if not picks:
        return
    rows = (len(picks) + cols - 1) // cols
    thumbs, label_h = [], 26
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
        draw.text((x + 6, y + thumb.height + 4),
                  f'#{p["n"]:02d}  {timecode(p["ts"])}', (235, 235, 235), font=font)
    sheet.save(out, quality=92)


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("video", type=Path)
    ap.add_argument("-o", "--outdir", type=Path, default=Path("stills"))
    ap.add_argument("-n", "--count", type=int, default=24,
                    help="how many stills to keep (default 24)")
    ap.add_argument("--rate", type=float, default=2.0,
                    help="candidate frames sampled per second (default 2)")
    ap.add_argument("--scene", type=float, default=0.25,
                    help="cut-detection sensitivity, 0-1 (default 0.25)")
    ap.add_argument("--min-gap", type=float, default=1.0,
                    help="minimum seconds between two keepers (default 1.0)")
    ap.add_argument("--no-autocrop", action="store_true",
                    help="keep letterbox bars instead of trimming them")
    ap.add_argument("--crops", default="4x5,9x16",
                    help="comma list of aspect crops, or 'none'")
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
        print(f"trimming padding -> {box['w']}x{box['h']} "
              f"(+{box['x']},{box['y']})")

    cuts = detect_cuts(args.video, args.scene)
    print(f"detected {len(cuts)} cuts -> {len(cuts) + 1} shots")

    eff_w = box["w"] if box else meta["width"]
    eff_h = box["h"] if box else meta["height"]
    sw = 320
    sh = max(2, round(sw * eff_h / eff_w) // 2 * 2)
    stamps, metrics = [], []
    for ts, frame in sample_candidates(args.video, args.rate, sw, sh, crop):
        stamps.append(ts)
        metrics.append(measure(frame))
    if not stamps:
        print("decoded no frames — is this really a video file?", file=sys.stderr)
        return 1
    print(f"scored {len(stamps)} candidate frames")

    # Drop fades and near-black transition frames before ranking.
    keep = [i for i, m in enumerate(metrics) if m["brightness"] > 12]
    if not keep:
        keep = list(range(len(metrics)))

    def col(name):
        return np.array([metrics[i][name] for i in keep], dtype=np.float64)

    score = (W_SHARP * rank(col("sharpness"))
             + W_CONTRAST * rank(col("contrast"))
             + W_COLOR * rank(col("color"))
             + W_CLIP * (1.0 - rank(col("clipped"))))

    # Best frame per shot, so we get coverage instead of ten stills of one setup.
    best: dict[int, tuple[float, float]] = {}
    for pos, i in enumerate(keep):
        shot = shot_index(stamps[i], cuts)
        if shot not in best or score[pos] > best[shot][1]:
            best[shot] = (stamps[i], float(score[pos]))

    ordered = sorted(best.values(), key=lambda t: -t[1])
    chosen: list[tuple[float, float]] = []
    for ts, sc in ordered:
        if len(chosen) >= args.count:
            break
        if all(abs(ts - t) >= args.min_gap for t, _ in chosen):
            chosen.append((ts, sc))
    chosen.sort(key=lambda t: t[0])

    args.outdir.mkdir(parents=True, exist_ok=True)
    full_dir = args.outdir / "full"
    full_dir.mkdir(exist_ok=True)

    picks = []
    for n, (ts, sc) in enumerate(chosen, 1):
        dest = full_dir / f"{n:02d}_{timecode(ts).replace(':', 'm')}.png"
        extract_full(args.video, ts, dest, crop)
        picks.append({"n": n, "ts": ts, "score": round(sc, 4), "path": dest})
        print(f"  #{n:02d}  {timecode(ts)}  score {sc:.3f}  {dest.name}")

    if args.crops.lower() != "none":
        for name in [c.strip() for c in args.crops.split(",") if c.strip()]:
            if name not in CROPS:
                print(f"  (skipping unknown crop {name})", file=sys.stderr)
                continue
            cdir = args.outdir / name
            cdir.mkdir(exist_ok=True)
            for p in picks:
                with Image.open(p["path"]) as im:
                    center_crop(im.convert("RGB"), CROPS[name]).save(
                        cdir / f'{p["n"]:02d}.jpg', quality=95, subsampling=0)
            print(f"cropped {len(picks)} stills to {name} -> {cdir}")

    sheet = args.outdir / "contact_sheet.jpg"
    contact_sheet(picks, sheet)
    (args.outdir / "picks.json").write_text(json.dumps(
        [{k: (str(v) if isinstance(v, Path) else v) for k, v in p.items()}
         for p in picks], indent=2))
    print(f"\n{len(picks)} stills in {args.outdir}\ncontact sheet: {sheet}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
