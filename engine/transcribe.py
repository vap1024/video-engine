#!/usr/bin/env python3
"""video-engine - ears: speech -> text with word timings (faster-whisper).

Usage: transcribe.py <audio-or-video> <out_prefix>
Writes <out_prefix>.json (segments + words) and <out_prefix>.srt.

Configuration (environment):
  VIDEO_ENGINE_WHISPER_MODEL  local model directory or hub model id.
                              Default: large-v3-turbo.
  VIDEO_ENGINE_LANGUAGE       language code. Default: ru.
"""
import json
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))
from video_engine.timing import fmt_srt  # noqa: E402


def main() -> None:
    src, prefix = sys.argv[1], sys.argv[2]
    from faster_whisper import WhisperModel

    model_id = os.environ.get("VIDEO_ENGINE_WHISPER_MODEL", "large-v3-turbo")
    language = os.environ.get("VIDEO_ENGINE_LANGUAGE", "ru")
    model = WhisperModel(model_id, device="cpu", compute_type="int8", cpu_threads=4)
    segments, info = model.transcribe(
        src, language=language, beam_size=5, vad_filter=True, word_timestamps=True
    )
    segs, srt = [], []
    for i, seg in enumerate(segments, 1):
        words = [
            {"w": w.word, "start": round(w.start, 3), "end": round(w.end, 3)}
            for w in (seg.words or [])
        ]
        segs.append({
            "start": round(seg.start, 3), "end": round(seg.end, 3),
            "text": seg.text.strip(), "words": words,
        })
        srt.append(f"{i}\n{fmt_srt(seg.start)} --> {fmt_srt(seg.end)}\n{seg.text.strip()}\n")
    with open(prefix + ".json", "w", encoding="utf-8") as f:
        json.dump({"language": info.language, "duration": info.duration,
                   "segments": segs}, f, ensure_ascii=False, indent=1)
    with open(prefix + ".srt", "w", encoding="utf-8") as f:
        f.write("\n".join(srt))
    print(f"OK {prefix}.json/.srt segments={len(segs)} dur={info.duration:.1f}s")


if __name__ == "__main__":
    main()
