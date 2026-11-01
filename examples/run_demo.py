#!/usr/bin/env python3
"""Synthetic demo: plan a 60-second episode and render its captions.

No ffmpeg, Whisper or Piper needed - voice durations and transcript
segments are synthetic fixtures, so the demo runs anywhere.

Usage: python examples/run_demo.py [--out report.md]
"""
import argparse
import json
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))
from video_engine.plan import plan_scenes, zoom_filter  # noqa: E402
from video_engine.timing import render_srt, filter_window  # noqa: E402

HERE = os.path.dirname(os.path.abspath(__file__))

# Synthetic voice durations (seconds) for four scenes.
VOICE = [9.57, 8.48, 9.40, 9.76]
SEGMENTS = [
    {"start": 11.0, "end": 15.2, "text": "Barsik runs the house and sleeps sixteen hours."},
    {"start": 22.5, "end": 26.9, "text": "Murzik hunts at night and ignores every rule."},
    {"start": 32.8, "end": 37.1, "text": "Pushok is white, round and permanently surprised."},
    {"start": 44.1, "end": 49.0, "text": "Together they are a gang with zero discipline."},
]


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", default=None)
    args = ap.parse_args()
    plan = plan_scenes(VOICE, total=60.0)
    keep = filter_window(SEGMENTS, plan["title"] + plan["prologue"] + 0.2,
                         60.0 - plan["end_dur"] - 0.2)
    srt = render_srt(keep)
    lines = [
        "# video-engine demo report",
        "",
        "Synthetic 60.0s episode planned from voice durations "
        + ", ".join(f"{v:.2f}s" for v in VOICE) + ".",
        "",
        "```json",
        json.dumps(plan, indent=1),
        "```",
        "",
        "First scene zoom filter:",
        "",
        "```",
        zoom_filter(plan["scene_dur"][0], zoom_in=True),
        "```",
        "",
        f"Captions kept: {len(keep)}/{len(SEGMENTS)} segments.",
        "",
        "```srt",
        srt,
        "```",
        "",
    ]
    report = "\n".join(lines)
    print(report)
    if args.out:
        with open(args.out, "w", encoding="utf-8") as f:
            f.write(report)
        print(f"wrote {args.out}", file=sys.stderr)


if __name__ == "__main__":
    main()
