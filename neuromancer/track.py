#!/usr/bin/env python3
"""Reading tracker for Neuromancer.

Usage:
    ./track.py status                 show where you are
    ./track.py log <chapter> <page>   record finishing a chapter on a page
    ./track.py history                list everything logged so far
    ./track.py set-pages <n>          set the page count for your edition
    ./track.py undo                   remove the most recent entry
"""

import json
import sys
from datetime import date, timedelta
from pathlib import Path

DATA = Path(__file__).parent / "progress.json"
BAR_WIDTH = 32


def load():
    return json.loads(DATA.read_text())


def save(state):
    DATA.write_text(json.dumps(state, indent=2) + "\n")


def all_chapters(state):
    return [ch for part in state["parts"] for ch in part["chapters"]]


def part_of(state, chapter):
    for part in state["parts"]:
        if chapter in part["chapters"]:
            return part["name"]
    return None


def bar(fraction):
    filled = round(fraction * BAR_WIDTH)
    return "[" + "#" * filled + "." * (BAR_WIDTH - filled) + "]"


def pace(entries):
    """Pages/day and a finish estimate, once there's enough history."""
    if len(entries) < 2:
        return None
    first = date.fromisoformat(entries[0]["date"])
    last = date.fromisoformat(entries[-1]["date"])
    days = (last - first).days
    if days < 1:
        return None
    return (entries[-1]["page"] - entries[0]["page"]) / days


def status(state):
    book = state["book"]
    total_pages = book["total_pages"]
    entries = state["entries"]
    chapters = all_chapters(state)

    print(f'{book["title"]} — {book["author"]}')

    if not entries:
        print(f"Nothing logged yet. {total_pages} pages ahead of you.")
        print('Log your first chapter with:  ./track.py log 1 <page>')
        return

    latest = entries[-1]
    page = latest["page"]
    done_chapters = sorted({e["chapter"] for e in entries})
    pct = min(page / total_pages, 1.0)

    print(f'{bar(pct)}  {pct * 100:.1f}%')
    print(f'page {page} of {total_pages}  ({total_pages - page} to go)')
    print(f'chapters finished: {len(done_chapters)} of {len(chapters)}')

    current = latest["chapter"] + 1
    if current in chapters:
        print(f'up next: chapter {current} — {part_of(state, current)}')
    else:
        print("that's the whole book. Finished.")

    left = total_pages - page
    rate = pace(entries)
    if left > 0 and rate and rate > 0:
        eta = date.today() + timedelta(days=round(left / rate))
        print(f'pace: {rate:.1f} pages/day — on track to finish around {eta:%b %d}')


def log(state, chapter, page):
    total_pages = state["book"]["total_pages"]
    chapters = all_chapters(state)

    if chapter not in chapters:
        sys.exit(f"Chapter {chapter} isn't in the book (1-{max(chapters)}).")
    if not 1 <= page <= total_pages:
        sys.exit(f"Page {page} is outside this edition (1-{total_pages}).")

    already = [e for e in state["entries"] if e["chapter"] == chapter]
    if already:
        print(f'(replacing an earlier entry for chapter {chapter})')
        state["entries"] = [e for e in state["entries"] if e["chapter"] != chapter]

    state["entries"].append(
        {"chapter": chapter, "page": page, "date": date.today().isoformat()}
    )
    state["entries"].sort(key=lambda e: e["chapter"])
    save(state)

    print(f'Logged: chapter {chapter} done, page {page} — {part_of(state, chapter)}\n')
    status(state)


def history(state):
    if not state["entries"]:
        print("Nothing logged yet.")
        return
    total_pages = state["book"]["total_pages"]
    prev = 0
    for e in state["entries"]:
        pct = e["page"] / total_pages * 100
        review = Path(__file__).parent / "reviews" / f'chapter-{e["chapter"]:02d}.md'
        mark = "  (review written)" if review.exists() else ""
        print(
            f'ch {e["chapter"]:>2}  p.{e["page"]:>3}  '
            f'{e["page"] - prev:>3} pages  {pct:>5.1f}%  {e["date"]}{mark}'
        )
        prev = e["page"]


def main():
    args = sys.argv[1:]
    if not args or args[0] in ("-h", "--help", "help"):
        print(__doc__)
        return

    state = load()
    cmd = args[0]

    if cmd == "status":
        status(state)
    elif cmd == "log":
        if len(args) != 3:
            sys.exit("Usage: ./track.py log <chapter> <page>")
        log(state, int(args[1]), int(args[2]))
    elif cmd == "history":
        history(state)
    elif cmd == "set-pages":
        if len(args) != 2:
            sys.exit("Usage: ./track.py set-pages <n>")
        state["book"]["total_pages"] = int(args[1])
        save(state)
        print(f'Edition set to {args[1]} pages.\n')
        status(state)
    elif cmd == "undo":
        if not state["entries"]:
            sys.exit("Nothing to undo.")
        dropped = state["entries"].pop()
        save(state)
        print(f'Removed chapter {dropped["chapter"]} (page {dropped["page"]}).\n')
        status(state)
    else:
        sys.exit(f"Unknown command: {cmd}\n\n{__doc__}")


if __name__ == "__main__":
    main()
