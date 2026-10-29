"""Scene planning and FFmpeg filter construction.

The planner is the heart of the engine: given measured voice durations
it lays out a fixed-total timeline (title, prologue, voiced scenes,
end card) so the finished video is exactly the requested length.
"""
from __future__ import annotations


def plan_scenes(voice_durations: list[float], total: float = 60.0,
                title: float = 5.0, prologue: float = 5.0,
                head: float = 1.0, tail: float = 0.9) -> dict:
    """Lay out scenes around measured voice clips.

    Each scene is head + voice + tail. The end card absorbs the
    remainder; it must land in [3, 9] seconds or the plan is invalid.
    """
    if not voice_durations:
        raise ValueError("at least one voice clip is required")
    if any(v <= 0 for v in voice_durations):
        raise ValueError("voice durations must be positive")
    scenes = [head + v + tail for v in voice_durations]
    end_dur = total - title - prologue - sum(scenes)
    if not (3.0 < end_dur < 9.0):
        raise ValueError(f"end card duration {end_dur:.2f}s out of range (3, 9)")
    starts, t = [], title + prologue
    for s in scenes:
        starts.append(round(t, 6))
        t += s
    return {
        "title": title, "prologue": prologue,
        "voice_dur": list(voice_durations),
        "scene_dur": scenes,
        "scene_starts": starts,
        "voice_starts": [round(s + head, 6) for s in starts],
        "end_dur": round(end_dur, 3),
        "total": total,
    }


def zoom_expression(zoom_in: bool) -> str:
    """zoompan z-expression: gentle 1.00->1.15 in, or 1.15->1.00 out."""
    if zoom_in:
        return "min(zoom+0.0009,1.15)"
    return "if(eq(on,0),1.15,max(zoom-0.0009,1.0))"


def zoom_filter(seconds: float, zoom_in: bool = True, width: int = 1280,
                height: int = 720, fps: int = 30) -> str:
    """Build the scale+crop+zoompan filter for one still-image scene."""
    frames = int(round(seconds * fps))
    if frames <= 0:
        raise ValueError("scene must be at least one frame")
    z = zoom_expression(zoom_in)
    return (
        f"[0:v]scale={width*2}:{height*2}:force_original_aspect_ratio=increase,"
        f"crop={width*2}:{height*2},"
        f"zoompan=z='{z}':d={frames}:x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)'"
        f":s={width}x{height}:fps={fps},format=yuv420p[v]"
    )


def lower_third_filter(scene_seconds: float) -> str:
    """Overlay filter that burns one badge into ONE scene.

    Pipeline lesson (see README failure log): overlaying several
    infinite-loop PNGs onto the whole timeline in a single graph
    nearly deadlocks ffmpeg. Badges are burned per scene instead,
    each with an explicit -loop 1 -t <scene duration> input.
    """
    if scene_seconds <= 0:
        raise ValueError("scene duration must be positive")
    return (
        "[1:v]format=rgba,fade=t=in:st=0.25:d=0.4:alpha=1,"
        "fade=t=out:st=3.65:d=0.4:alpha=1[lt];"
        "[0:v][lt]overlay=0:0:shortest=1,format=yuv420p[v]"
    )
