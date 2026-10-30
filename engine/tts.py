#!/usr/bin/env python3
"""video-engine - voice: text -> wav (Piper, offline).

Usage: tts.py <text_file> <out_wav>
Prints the wav duration as the last line: DUR=<sec> (measured by ffprobe).

Configuration (environment, both required - no machine-local defaults):
  PIPER_BIN    path to the piper executable
  PIPER_VOICE  path to a Piper voice model (.onnx), e.g. a medium
               single-speaker voice for your language
"""
import os
import subprocess
import sys


def main() -> None:
    piper = os.environ.get("PIPER_BIN")
    voice = os.environ.get("PIPER_VOICE")
    if not piper or not voice:
        raise SystemExit("set PIPER_BIN and PIPER_VOICE (see module docstring)")
    text_file, out_wav = sys.argv[1], sys.argv[2]
    text = open(text_file, encoding="utf-8").read().strip()
    subprocess.run([piper, "-m", voice, "-f", out_wav], input=text.encode(),
                   check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    dur = subprocess.run(
        ["ffprobe", "-v", "error", "-show_entries", "format=duration",
         "-of", "csv=p=0", out_wav], capture_output=True, text=True,
    ).stdout.strip()
    print(f"DUR={float(dur):.2f}")


if __name__ == "__main__":
    main()
