"""Timing and subtitle helpers extracted from the production pipeline.

Pure functions, no I/O beyond string formatting, fully unit-tested.
"""
from __future__ import annotations


def fmt_srt(t: float) -> str:
    """Format seconds as an SRT timestamp HH:MM:SS,mmm."""
    if t < 0:
        raise ValueError("timestamp must be >= 0")
    h = int(t // 3600)
    m = int((t % 3600) // 60)
    s = int(t % 60)
    ms = int(round((t - int(t)) * 1000))
    if ms == 1000:  # rounding carry
        ms = 0
        s += 1
        if s == 60:
            s = 0
            m += 1
            if m == 60:
                m = 0
                h += 1
    return f"{h:02d}:{m:02d}:{s:02d},{ms:03d}"


def render_srt(segments: list[dict]) -> str:
    """Render segments [{start, end, text}] as an SRT document."""
    blocks = []
    for i, seg in enumerate(segments, 1):
        if seg["end"] < seg["start"]:
            raise ValueError(f"segment {i}: end before start")
        blocks.append(f"{i}\n{fmt_srt(seg['start'])} --> {fmt_srt(seg['end'])}\n{seg['text'].strip()}\n")
    return "\n".join(blocks)


def filter_window(segments: list[dict], start: float, end: float) -> list[dict]:
    """Keep segments fully relevant to [start, end): end > start and start < end."""
    return [s for s in segments if s["end"] > start and s["start"] < end]
