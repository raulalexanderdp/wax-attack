# Neuromancer — reading companion

A place to track how far into the book you are and to keep a review of every
chapter as you finish it.

## The loop

1. You finish a chapter and tell me the chapter number and the page you're on.
2. I log it, and write a review into `reviews/chapter-NN.md`.
3. `track.py status` tells you what percent of the book you've done.

You never have to run anything yourself — just tell me "finished chapter 3,
I'm on page 47" and I'll do both halves. The commands are here for when you
want to check your own progress without me.

## Commands

```
./track.py status              where you are, as a percentage
./track.py log <chapter> <page>  record finishing a chapter
./track.py history             every chapter logged, with pages and dates
./track.py set-pages <n>       set the page count for your edition
./track.py undo                remove the most recent entry
```

Example:

```
$ ./track.py log 1 23
Logged: chapter 1 done, page 23 — Part One: Chiba City Blues

Neuromancer — William Gibson
[###.............................]  8.5%
page 23 of 271  (248 to go)
chapters finished: 1 of 24
up next: chapter 2 — Part One: Chiba City Blues
```

Once there are a few entries it also estimates your pace and a finish date.

## Your edition

Percentage is page-based, so it depends on which copy you're holding. The
default is the Ace mass-market paperback at **271 pages**. If your copy has a
different page count, set it once:

```
./track.py set-pages 320
```

Everything already logged keeps working — the percentages just recalculate.

## The chapter map

`progress.json` has the book's structure: 24 chapters across four parts and a
coda.

| Part | Chapters |
| --- | --- |
| Part One: Chiba City Blues | 1–3 |
| Part Two: The Shopping Expedition | 4–7 |
| Part Three: Midnight in the Rue Jules Verne | 8–14 |
| Part Four: The Straylight Run | 15–23 |
| Coda: Departure and Arrival | 24 |

If your edition divides things differently, edit the `parts` list in
`progress.json` and the tracker follows it.

## Reviews

One file per chapter in `reviews/`, written after you've read it. They stay
strictly behind your bookmark — nothing in a review gives away anything past
the chapter it covers. See `reviews/README.md` for the format.
