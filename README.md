# video-engine

Edit video with code, not a timeline editor. An agent (or a script)
directs; free local tools do the work: **faster-whisper** transcribes,
**Piper** voices, **FFmpeg** cuts and burns, **Remotion** renders only
the animated inserts (titles, end cards, lower-third badges). The
pipeline in this repo assembled a finished 60.0-second test episode
end to end: voice, scenes, badges, subtitles and final mix.

## Why inserts only

Rendering a whole video through a frame-by-frame web stack is slow.
Rendering *only the inserts* (390 frames in the test episode) took
~33 seconds on a modest CPU, versus ~10 minutes for a full
frame-by-frame pass of the base. The base is plain FFmpeg: stills with
a Ken Burns zoom, concatenated, mixed, captioned.

## Pipeline

1. **Ears** - `engine/transcribe.py`: faster-whisper, word timings ->
   `.json` + `.srt`. Model and language via environment
   (`VIDEO_ENGINE_WHISPER_MODEL`, `VIDEO_ENGINE_LANGUAGE`).
2. **Voice** - `engine/tts.py`: Piper, fully offline. Binary and voice
   model via `PIPER_BIN` / `PIPER_VOICE` (no machine-local defaults).
3. **Planner** - `src/video_engine/plan.py`: from measured voice
   durations it lays out a fixed-total timeline (title, prologue,
   voiced scenes, end card that absorbs the remainder and must land
   in 3-9s, else the plan is rejected). Also builds the zoompan and
   per-scene badge-overlay filters.
4. **Animator** - `remotion/` (Remotion 4, React): `TitleCard`,
   `EndCard`, `LowerThird` compositions only. Rendered through
   `remotion/render.mjs` inside `engine/render-remotion.sh`.
5. **Assembly** - badges are burned into each scene separately, then
   concat, audio mix, subtitle burn-in (libass).

## Quick start (offline demo)

Requires Python 3.11+. No dependencies, no ffmpeg needed:

```console
python examples/run_demo.py
python -m pytest -q        # or: python -m unittest discover -s tests
```

The demo plans a synthetic 60.0s episode from four voice durations,
keeps the caption segments inside the voiced window, and prints the
plan, the first scene's zoom filter and the SRT. Expected output is
committed at `examples/demo_report.md`.

## Full pipeline

Prerequisites: ffmpeg/ffprobe, a faster-whisper model, a Piper voice,
Node 18+ with the Remotion project (`remotion/`, `npm install`,
`npx remotion browser ensure` for its Chrome Headless Shell).

```console
export PIPER_BIN=/path/to/piper PIPER_VOICE=/path/to/voice.onnx
python engine/tts.py scene1.txt scene1.wav
python engine/transcribe.py mix.wav captions
engine/render-remotion.sh still LowerThird badge.png '{"name":"NAME","role":"ROLE","color":"#e8873a"}'
engine/render-remotion.sh video TitleCard title.mp4
```

## Failure log (honest)

- **System Chromium blocked `http://localhost`** on the original host
  (`ERR_BLOCKED_BY_LOCAL_NETWORK_ACCESS_CHECKS`): Remotion only works
  with its own Chrome Headless Shell there.
- **"No available ports found"**: Remotion picks a port by probing
  connects to `0.0.0.0` / `::`; behind a transparent proxy those probes
  always "succeed". Fixed by rendering inside a fresh network
  namespace (`unshare -Urn`) - see `engine/render-remotion.sh`.
- **Near-deadlock from badge overlays**: several infinite `-loop 1`
  PNG inputs in one overlay graph over the whole timeline took ~6
  minutes for 60 seconds. Burning each badge into its own scene (with
  an explicit `-t <scene>`) takes seconds. Encoded in
  `lower_third_filter()` and its test.
- **Remotion 4.0.x `chromiumOptions` has no `args` field** - custom
  Chrome flags cannot be passed through it.
- **Whisper on synthetic (TTS) speech** misheard proper names in the
  test episode; on real speech, verify names in captions separately.
- The demo episode's cat photos are deliberately *not* shipped; the
  Remotion cards reference a `cat-group.webp` still you supply in
  `remotion/public/`.

## Layout

```
engine/    transcribe.py, tts.py, render-remotion.sh
remotion/  render.mjs + src/ (TitleCard, EndCard, LowerThird)
src/       video_engine/ - planner, timing/SRT helpers (tested)
examples/  run_demo.py + committed demo_report.md
tests/     unit tests for planner and timing
```

## License

MIT
