#!/usr/bin/env python3
"""Render progress.json + reviews/*.md into a single self-contained page.

    ./build.py            writes reading-log.html

The page is generated, never hand-edited — it can't drift from the data.
"""

import html
import json
import re
from datetime import date, timedelta
from pathlib import Path

HERE = Path(__file__).parent
OUT = HERE / "reading-log.html"


# --------------------------------------------------------------------------
# a small markdown renderer, scoped to the subset the reviews actually use
# --------------------------------------------------------------------------

def inline(text):
    out = html.escape(text)
    out = re.sub(r"`([^`]+)`", r"<code>\1</code>", out)
    out = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", out)
    out = re.sub(r"\*(.+?)\*", r"<em>\1</em>", out)
    return out


def render_markdown(src):
    """Returns (title, body_html). The leading '# ' line becomes the title."""
    lines = src.splitlines()
    title = ""
    if lines and lines[0].startswith("# "):
        title = lines.pop(0)[2:].strip()

    out, para, bullets, table = [], [], [], []

    def flush_para():
        if para:
            out.append(f'<p>{inline(" ".join(para))}</p>')
            para.clear()

    def flush_bullets():
        if bullets:
            items = "".join(f"<li>{inline(b)}</li>" for b in bullets)
            out.append(f"<ul>{items}</ul>")
            bullets.clear()

    def flush_table():
        if not table:
            return
        rows = [[c.strip() for c in r.strip().strip("|").split("|")] for r in table]
        head, body = rows[0], rows[2:]  # rows[1] is the --- separator
        th = "".join(f"<th>{inline(c)}</th>" for c in head)
        trs = "".join(
            "<tr>" + "".join(f"<td>{inline(c)}</td>" for c in r) + "</tr>"
            for r in body
        )
        out.append(
            '<div class="scroller"><table><thead><tr>'
            f"{th}</tr></thead><tbody>{trs}</tbody></table></div>"
        )
        table.clear()

    def flush_all():
        flush_para()
        flush_bullets()
        flush_table()

    for raw in lines:
        line = raw.rstrip()

        if line.startswith("|"):
            flush_para()
            flush_bullets()
            table.append(line)
            continue
        flush_table()

        if not line.strip():
            flush_para()
            flush_bullets()
        elif line.startswith("## "):
            flush_all()
            out.append(f'<h3>{inline(line[3:].strip())}</h3>')
        elif line.startswith("- "):
            flush_para()
            bullets.append(line[2:].strip())
        elif bullets and line.startswith("  "):
            bullets[-1] += " " + line.strip()   # continuation of a bullet
        else:
            flush_bullets()
            para.append(line.strip())

    flush_all()
    return title, "\n".join(out)


# --------------------------------------------------------------------------
# data
# --------------------------------------------------------------------------

def load():
    state = json.loads((HERE / "progress.json").read_text())
    entries = state["entries"]
    total = state["book"]["total_pages"]
    chapters = [c for p in state["parts"] for c in p["chapters"]]
    read = sorted({e["chapter"] for e in entries})
    page = entries[-1]["page"] if entries else 0

    pace = None
    if len(entries) >= 2:
        span = (
            date.fromisoformat(entries[-1]["date"])
            - date.fromisoformat(entries[0]["date"])
        ).days
        if span >= 1:
            rate = (entries[-1]["page"] - entries[0]["page"]) / span
            if rate > 0:
                pace = (rate, date.today() + timedelta(days=round((total - page) / rate)))

    return state, entries, total, chapters, read, page, pace


def part_name(state, chapter):
    for p in state["parts"]:
        if chapter in p["chapters"]:
            return p["name"]
    return ""


# --------------------------------------------------------------------------
# page pieces
# --------------------------------------------------------------------------

def stat(value, label, mono=True):
    cls = "stat-value mono" if mono else "stat-value"
    return (
        f'<div class="stat"><div class="{cls}">{value}</div>'
        f'<div class="stat-label">{label}</div></div>'
    )


def build_stats(state, total, chapters, read, page, pace):
    cells = [
        stat(f"{page}<span class='dim'> / {total}</span>", "page"),
        stat(f"{total - page}", "pages left"),
        stat(f"{len(read)}<span class='dim'> / {len(chapters)}</span>", "chapters"),
    ]
    if pace:
        rate, eta = pace
        cells.append(stat(f"{rate:.1f}", "pages per day"))
        cells.append(stat(f"{eta:%b %-d}", "projected finish"))
    return "".join(cells)


def build_strip(state, chapters, read):
    short = ["One", "Two", "Three", "Four", "Coda"]
    nxt = (max(read) + 1) if read else 1
    groups = []
    for i, part in enumerate(state["parts"]):
        cells = []
        for ch in part["chapters"]:
            if ch in read:
                cells.append(
                    f'<a class="cell done" href="#ch-{ch:02d}" '
                    f'title="Chapter {ch} — review written"><span>{ch}</span></a>'
                )
            elif ch == nxt:
                cells.append(
                    f'<div class="cell next" title="Chapter {ch} — up next">'
                    f"<span>{ch}</span></div>"
                )
            else:
                cells.append(
                    f'<div class="cell" title="Chapter {ch}"><span>{ch}</span></div>'
                )
        label = short[i] if i < len(short) else part["name"]
        groups.append(
            f'<div class="group" style="flex-grow:{len(part["chapters"])}" '
            f'title="{html.escape(part["name"])}">'
            f'<div class="group-cells">{"".join(cells)}</div>'
            f'<div class="group-label">{html.escape(label)}</div></div>'
        )
    return "".join(groups)


def build_reviews(state):
    files = sorted((HERE / "reviews").glob("chapter-*.md"))
    if not files:
        return (
            '<p class="empty">No chapter reviews yet. The first one lands here '
            "once you finish chapter 1.</p>"
        )
    out = []
    for f in files:
        ch = int(re.search(r"(\d+)", f.name).group(1))
        title, body = render_markdown(f.read_text())
        heading = title or f"Chapter {ch}"
        # split "Chapter N — Part name" into a number and a name
        m = re.match(r"Chapter\s+(\d+)\s*—\s*(.+)", heading)
        num, name = (m.group(1), m.group(2)) if m else (str(ch), heading)
        out.append(
            f'<article class="review" id="ch-{ch:02d}">'
            f'<header class="review-head">'
            f'<div class="review-num mono">{html.escape(num)}</div>'
            f'<h2>{html.escape(name)}</h2></header>'
            f'<div class="prose">{body}</div></article>'
        )
    return "".join(out)


# --------------------------------------------------------------------------

CSS = """
:root {
  --paper:   #eaedea;
  --surface: #f4f6f3;
  --ink:     #14181a;
  --muted:   #5c6f6a;
  --line:    #cdd4d0;
  --amber:   #b45c12;
  --amber-soft: rgba(180, 92, 18, 0.14);
  --measure: 66ch;
}
:root:not([data-theme="light"]) { color-scheme: light dark; }
@media (prefers-color-scheme: dark) {
  :root:not([data-theme="light"]) {
    --paper:   #0e1112;
    --surface: #171b1c;
    --ink:     #dfe4e1;
    --muted:   #7f938d;
    --line:    #2a3133;
    --amber:   #e8913c;
    --amber-soft: rgba(232, 145, 60, 0.16);
  }
}
:root[data-theme="dark"] {
  --paper:   #0e1112;
  --surface: #171b1c;
  --ink:     #dfe4e1;
  --muted:   #7f938d;
  --line:    #2a3133;
  --amber:   #e8913c;
  --amber-soft: rgba(232, 145, 60, 0.16);
}

body {
  margin: 0;
  background: var(--paper);
  color: var(--ink);
  font-family: Spectral, Georgia, "Times New Roman", serif;
  font-size: 17px;
  line-height: 1.65;
  -webkit-font-smoothing: antialiased;
}
.mono { font-family: "IBM Plex Mono", ui-monospace, "SFMono-Regular", monospace; }
.wrap {
  max-width: 60rem;
  margin: 0 auto;
  padding: 0 1.5rem 6rem;
  display: flex;
  flex-direction: column;
  gap: 3.5rem;
}

/* masthead ------------------------------------------------------------- */
.masthead {
  position: relative;
  overflow: hidden;
  margin: 0 -1.5rem;
  padding: 4.5rem 1.5rem 3rem;
  border-bottom: 1px solid var(--line);
}
#static {
  position: absolute;
  inset: 0;
  width: 100%;
  height: 100%;
  opacity: 0.055;
  pointer-events: none;
}
.masthead > * { position: relative; }
.eyebrow {
  font-family: "IBM Plex Mono", ui-monospace, monospace;
  font-size: 0.7rem;
  letter-spacing: 0.22em;
  text-transform: uppercase;
  color: var(--muted);
  margin: 0 0 1.25rem;
}
.masthead h1 {
  font-family: Archivo, "Helvetica Neue", Arial, sans-serif;
  font-weight: 800;
  font-size: clamp(2.75rem, 9vw, 5rem);
  letter-spacing: -0.035em;
  line-height: 0.94;
  text-wrap: balance;
  margin: 0;
}
.byline {
  margin: 0.9rem 0 0;
  color: var(--muted);
  font-size: 0.95rem;
}
.epigraph {
  margin: 2.25rem 0 0;
  padding-left: 1rem;
  border-left: 2px solid var(--amber);
  max-width: 42ch;
  font-style: italic;
  color: var(--muted);
  font-size: 0.95rem;
  line-height: 1.5;
}

/* progress ------------------------------------------------------------- */
.progress { display: flex; flex-direction: column; gap: 1.75rem; }
.pct-row { display: flex; align-items: baseline; gap: 1rem; flex-wrap: wrap; }
.pct {
  font-family: Archivo, Arial, sans-serif;
  font-weight: 800;
  font-size: clamp(3rem, 12vw, 5.5rem);
  line-height: 0.85;
  letter-spacing: -0.04em;
  color: var(--amber);
  font-variant-numeric: tabular-nums;
}
.pct sub {
  font-size: 0.3em;
  font-weight: 700;
  letter-spacing: 0.02em;
  vertical-align: baseline;
  bottom: 0;
}
.pct-note {
  font-family: "IBM Plex Mono", monospace;
  font-size: 0.75rem;
  letter-spacing: 0.14em;
  text-transform: uppercase;
  color: var(--muted);
}
.meter {
  height: 6px;
  background: var(--line);
  border-radius: 999px;
  overflow: hidden;
}
.meter-fill {
  height: 100%;
  width: 0;
  background: var(--amber);
  border-radius: 999px;
  transition: width 1.1s cubic-bezier(0.2, 0.7, 0.3, 1);
}
@media (prefers-reduced-motion: reduce) { .meter-fill { transition: none; } }

.stats {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(7.5rem, 1fr));
  gap: 1.25rem 1.75rem;
  margin: 0;
}
.stat-value {
  font-size: 1.6rem;
  font-weight: 500;
  letter-spacing: -0.01em;
  font-variant-numeric: tabular-nums;
  line-height: 1.2;
}
.stat-value .dim { color: var(--muted); font-size: 0.75em; }
.stat-label {
  font-family: "IBM Plex Mono", monospace;
  font-size: 0.68rem;
  letter-spacing: 0.16em;
  text-transform: uppercase;
  color: var(--muted);
  margin-top: 0.3rem;
}

/* chapter strip -------------------------------------------------------- */
.section-head {
  display: flex;
  justify-content: space-between;
  align-items: baseline;
  gap: 1rem;
  border-top: 1px solid var(--line);
  padding-top: 1rem;
  margin-bottom: 1.5rem;
}
.section-head h2 {
  font-family: Archivo, Arial, sans-serif;
  font-size: 0.78rem;
  font-weight: 700;
  letter-spacing: 0.18em;
  text-transform: uppercase;
  margin: 0;
}
.section-head .hint {
  font-family: "IBM Plex Mono", monospace;
  font-size: 0.7rem;
  color: var(--muted);
}
.strip { display: flex; gap: 0.85rem; align-items: stretch; }
.group { display: flex; flex-direction: column; gap: 0.5rem; min-width: 0; }
.group-cells { display: flex; gap: 3px; }
.group-label {
  font-family: "IBM Plex Mono", monospace;
  font-size: 0.65rem;
  letter-spacing: 0.12em;
  text-transform: uppercase;
  color: var(--muted);
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}
.cell {
  flex: 1 1 0;
  min-width: 0;
  height: 2.6rem;
  border: 1px solid var(--line);
  border-radius: 2px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-family: "IBM Plex Mono", monospace;
  font-size: 0.62rem;
  color: var(--muted);
  text-decoration: none;
}
.cell span { opacity: 0.75; }
.cell.done {
  background: var(--amber);
  border-color: var(--amber);
  color: var(--paper);
}
.cell.done span { opacity: 0.9; }
.cell.done:hover { filter: brightness(1.12); }
.cell.next { border-color: var(--amber); background: var(--amber-soft); }
.cell.next span { color: var(--amber); opacity: 1; }
a.cell:focus-visible { outline: 2px solid var(--amber); outline-offset: 2px; }

/* reviews -------------------------------------------------------------- */
.reviews { display: flex; flex-direction: column; gap: 3rem; }
.review { scroll-margin-top: 2rem; }
.review-head {
  display: flex;
  align-items: baseline;
  gap: 1rem;
  padding-bottom: 1rem;
  border-bottom: 1px solid var(--line);
  margin-bottom: 1.75rem;
}
.review-num {
  font-size: 0.8rem;
  color: var(--amber);
  letter-spacing: 0.1em;
  flex: none;
}
.review-num::before { content: "CH "; opacity: 0.55; }
.review-head h2 {
  font-family: Archivo, Arial, sans-serif;
  font-size: clamp(1.35rem, 3.4vw, 1.9rem);
  font-weight: 700;
  letter-spacing: -0.02em;
  line-height: 1.15;
  text-wrap: balance;
  margin: 0;
}
.prose { max-width: var(--measure); }
.prose > * + * { margin-top: 1.1rem; }
.prose h3 {
  font-family: Archivo, Arial, sans-serif;
  font-size: 0.75rem;
  font-weight: 700;
  letter-spacing: 0.16em;
  text-transform: uppercase;
  color: var(--muted);
  margin-top: 2.4rem;
}
.prose p { margin: 0; }
.prose p:first-child em { color: var(--muted); font-size: 0.9rem; }
.prose strong { font-weight: 600; }
.prose ul { margin: 0; padding-left: 1.1rem; }
.prose li { margin-top: 0.5rem; }
.prose li::marker { color: var(--amber); }
.prose code {
  font-family: "IBM Plex Mono", monospace;
  font-size: 0.85em;
  background: var(--surface);
  padding: 0.1em 0.35em;
  border-radius: 3px;
}
.scroller { overflow-x: auto; }
.prose table {
  border-collapse: collapse;
  width: 100%;
  font-size: 0.92rem;
}
.prose th {
  text-align: left;
  font-family: "IBM Plex Mono", monospace;
  font-size: 0.62rem;
  font-weight: 500;
  letter-spacing: 0.16em;
  text-transform: uppercase;
  color: var(--muted);
  padding: 0 1.25rem 0.6rem 0;
  border-bottom: 1px solid var(--line);
}
.prose td {
  padding: 0.6rem 1.25rem 0.6rem 0;
  border-bottom: 1px solid var(--line);
  vertical-align: top;
}
.prose tbody tr:last-child td { border-bottom: none; }
.prose td:first-child {
  font-family: "IBM Plex Mono", monospace;
  font-size: 0.82rem;
  color: var(--amber);
  white-space: nowrap;
}
.empty { color: var(--muted); font-style: italic; }
.colophon {
  border-top: 1px solid var(--line);
  padding-top: 1rem;
  font-family: "IBM Plex Mono", monospace;
  font-size: 0.68rem;
  letter-spacing: 0.08em;
  color: var(--muted);
}
"""

SHELL = """<title>Neuromancer Reading Log</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Archivo:wght@400;700;800&family=IBM+Plex+Mono:wght@400;500&family=Spectral:ital,wght@0,400;0,600;1,400&display=swap">
<style>{{CSS}}</style>

<div class="wrap">
  <header class="masthead">
    <canvas id="static" aria-hidden="true"></canvas>
    <p class="eyebrow">Reading log</p>
    <h1>Neuromancer</h1>
    <p class="byline">William Gibson &middot; {{TOTAL}}-page edition &middot; 24 chapters</p>
    <p class="epigraph">The sky above the port was the color of television, tuned to a dead channel.</p>
  </header>

  <section class="progress" aria-label="Progress">
    <div class="pct-row">
      <div class="pct">{{PCT}}<sub>%</sub></div>
      <div class="pct-note">{{POSITION}}</div>
    </div>
    <div class="meter"><div class="meter-fill" data-pct="{{PCT}}"></div></div>
    <div class="stats">{{STATS}}</div>
  </section>

  <section aria-label="Chapter map">
    <div class="section-head">
      <h2>The book</h2>
      <span class="hint">{{HINT}}</span>
    </div>
    <div class="strip">{{STRIP}}</div>
  </section>

  <section class="reviews" aria-label="Chapter reviews">
    <div class="section-head">
      <h2>Reviews</h2>
      <span class="hint">nothing past your bookmark</span>
    </div>
    {{REVIEWS}}
  </section>

  <p class="colophon">Generated from progress.json &middot; last logged {{DATE}}</p>
</div>

<script>
  (function () {
    var c = document.getElementById('static');
    if (c) {
      var w = c.width = c.offsetWidth, h = c.height = c.offsetHeight;
      var ctx = c.getContext('2d'), img = ctx.createImageData(w, h), d = img.data;
      for (var i = 0; i < d.length; i += 4) {
        var v = (Math.random() * 255) | 0;
        d[i] = d[i + 1] = d[i + 2] = v;
        d[i + 3] = 255;
      }
      ctx.putImageData(img, 0, 0);
    }
    var fill = document.querySelector('.meter-fill');
    if (fill) {
      requestAnimationFrame(function () {
        fill.style.width = fill.dataset.pct + '%';
      });
    }
  })();
</script>
"""


def main():
    state, entries, total, chapters, read, page, pace = load()
    pct = (page / total * 100) if total else 0
    nxt = (max(read) + 1) if read else 1

    if not read:
        position = "not started"
        hint = "24 chapters, five parts"
    elif nxt in chapters:
        position = f"up next — chapter {nxt}, {part_name(state, nxt)}"
        hint = "filled = read · click to jump to a review"
    else:
        position = "finished"
        hint = "click to jump to a review"

    page_html = (
        SHELL.replace("{{CSS}}", CSS)
        .replace("{{TOTAL}}", str(total))
        .replace("{{PCT}}", f"{pct:.1f}")
        .replace("{{POSITION}}", html.escape(position))
        .replace("{{STATS}}", build_stats(state, total, chapters, read, page, pace))
        .replace("{{HINT}}", html.escape(hint))
        .replace("{{STRIP}}", build_strip(state, chapters, read))
        .replace("{{REVIEWS}}", build_reviews(state))
        .replace("{{DATE}}", entries[-1]["date"] if entries else "—")
    )
    OUT.write_text(page_html)
    print(f"wrote {OUT.name}  ({len(page_html):,} bytes, {len(read)} review(s))")


if __name__ == "__main__":
    main()
