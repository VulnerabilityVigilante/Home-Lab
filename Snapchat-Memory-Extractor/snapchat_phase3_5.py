#!/usr/bin/env python3

import subprocess
from pathlib import Path
import argparse
import zipfile

EXTRACTED = Path("extracted_videos")
OUTPUT = Path("videos_rendered_fixed")
MEDIA_DIR = Path(".")

def run(cmd, dry):
    if dry:
        print(cmd)
    else:
        subprocess.run(cmd, shell=True, check=True)

# ------------------------------------------------------------
# ZIP Extraction (video assets only)
# ------------------------------------------------------------

def extract_zip_videos(dry):
    EXTRACTED.mkdir(exist_ok=True)

    for z in MEDIA_DIR.glob("*.zip"):
        try:
            with zipfile.ZipFile(z) as zipf:
                names = zipf.namelist()
                targets = [
                    n for n in names
                    if n.endswith("-main.mp4") or n.endswith("-overlay.png")
                ]

                if not targets:
                    continue

                for name in targets:
                    dest = EXTRACTED / Path(name).name
                    if dest.exists():
                        continue

                    if dry:
                        print(f"[ZIP] extract {name} from {z.name}")
                    else:
                        zipf.extract(name, EXTRACTED)

        except zipfile.BadZipFile:
            continue

# ------------------------------------------------------------
# Video Reconstruction + Metadata Preservation
# ------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()

    OUTPUT.mkdir(exist_ok=True)

    print("[INFO] Extracting ZIP video assets")
    extract_zip_videos(args.dry_run)

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

        # ----------------------------------------------------
        # Step 1: Render video
        # ----------------------------------------------------
        ffmpeg_cmd = f"""
ffmpeg -y \
  -i "{main}" \
  -i "{overlay}" \
  -map_metadata 0 \
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

        run(ffmpeg_cmd, args.dry_run)

        # ----------------------------------------------------
        # Step 2: Rehydrate ALL timestamps from source MP4
        # ----------------------------------------------------
        exif_cmd = (
            f'exiftool -overwrite_original '
            f'-TagsFromFile "{main}" '
            f'-CreateDate -ModifyDate '
            f'-TrackCreateDate -TrackModifyDate '
            f'-MediaCreateDate -MediaModifyDate '
            f'"{out}"'
        )

        run(exif_cmd, args.dry_run)

    print(f"\nDONE — queued {total} videos (metadata preserved)")

if __name__ == "__main__":
    main()

