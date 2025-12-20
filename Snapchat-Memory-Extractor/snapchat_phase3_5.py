#!/usr/bin/env python3

import subprocess
from pathlib import Path
import argparse

EXTRACTED = Path("extracted_videos")
OUTPUT = Path("videos_rendered_fixed")

def run(cmd, dry):
    if dry:
        print(cmd)
    else:
        subprocess.run(cmd, shell=True, check=True)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()

    OUTPUT.mkdir(exist_ok=True)

    mains = sorted(EXTRACTED.glob("*-main.mp4"))
    total = 0

    for main in mains:
        base_id = main.name.replace("-main.mp4", "")
        overlay = EXTRACTED / f"{base_id}-overlay.png"
        out = OUTPUT / f"{base_id}.mp4"

        if not overlay.exists():
            continue

        if out.exists():
            continue

        print(f"[VIDEO] {base_id}")
        total += 1

        cmd = f"""
ffmpeg -y \
  -i "{main}" \
  -i "{overlay}" \
  -filter_complex "\
    [0:v]scale=720:1280:force_original_aspect_ratio=decrease,\
    pad=720:1280:(ow-iw)/2:(oh-ih)/2[base]; \
    [1:v]scale=720:1280[overlay]; \
    [base][overlay]overlay=0:0" \
  -map 0:a? \
  -c:v libx264 -crf 18 -preset slow \
  -c:a copy \
  "{out}"
""".strip()

        run(cmd, args.dry_run)

    print(f"\nDONE — queued {total} videos")

if __name__ == "__main__":
    main()
