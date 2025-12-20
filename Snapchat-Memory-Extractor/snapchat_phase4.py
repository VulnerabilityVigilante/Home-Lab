#!/usr/bin/env python3

import argparse
import subprocess
from pathlib import Path

RENDERED_DIR = Path("videos_rendered")
FIXED_DIR = Path("videos_rendered_fixed")
FINAL_DIR = Path("final_videos")


def run(cmd, dry_run=False):
    if dry_run:
        print(" ".join(cmd))
        return
    subprocess.run(cmd, check=True)


def main():
    parser = argparse.ArgumentParser(
        description="Phase 4: Copy metadata to fixed videos, normalize MediaCreateDate, and finalize outputs"
    )
    parser.add_argument("--dry-run", action="store_true", help="Print commands without executing")
    args = parser.parse_args()

    if not FIXED_DIR.exists():
        print(f"[ERROR] Missing directory: {FIXED_DIR}")
        return

    FINAL_DIR.mkdir(exist_ok=True)

    fixed_videos = sorted(FIXED_DIR.glob("*.mp4"))
    if not fixed_videos:
        print("[INFO] No fixed videos found")
        return

    print(f"[INFO] Processing {len(fixed_videos)} videos")

    # ------------------------------------------------------------
    # Step 1: Copy metadata from rendered → fixed (NO BACKUPS)
    # ------------------------------------------------------------
    for fixed in fixed_videos:
        src = RENDERED_DIR / fixed.name
        if not src.exists():
            print(f"[WARN] Missing source video: {src.name}")
            continue

        print(f"[VIDEO] {fixed.name}")
        run([
            "exiftool",
            "-overwrite_original",
            "-TagsFromFile", str(src),
            "-CreateDate",
            "-TrackCreateDate",
            "-GPSCoordinates",
            str(fixed)
        ], args.dry_run)

    # ------------------------------------------------------------
    # Step 2: Normalize MediaCreateDate (NO BACKUPS)
    # ------------------------------------------------------------
    print("[INFO] Normalizing MediaCreateDate")
    run([
        "exiftool",
        "-overwrite_original",
        "-if", '$MediaCreateDate eq "0000:00:00 00:00:00"',
        "-MediaCreateDate<CreateDate",
        str(FIXED_DIR / "*.mp4")
    ], args.dry_run)

    # ------------------------------------------------------------
    # Step 3: Move finalized videos → final_videos/
    # ------------------------------------------------------------
    print("[INFO] Finalizing videos into final_videos/")

    for fixed in fixed_videos:
        dest = FINAL_DIR / fixed.name

        if dest.exists():
            # Idempotency: don't overwrite
            continue

        if args.dry_run:
            print(f"mv {fixed} {dest}")
        else:
            fixed.rename(dest)

    print("DONE — Phase 4 complete (final videos ready, Immich-safe)")


if __name__ == "__main__":
    main()

