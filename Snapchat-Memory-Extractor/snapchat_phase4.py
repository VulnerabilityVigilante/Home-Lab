#!/usr/bin/env python3

import argparse
import subprocess
from pathlib import Path

RENDERED_PHOTOS = Path("rendered")
VIDEO_FIXED = Path("videos_rendered_fixed")

FINAL_PHOTOS = Path("final_photos")
FINAL_VIDEOS = Path("final_videos")

SKIP_DIRS = {
    "tmp",
    "rendered",
    "videos_rendered",
    "videos_rendered_fixed",
    "final_photos",
    "final_videos",
    "extracted_videos",
}

def run(cmd, dry):
    if dry:
        print(" ".join(cmd))
    else:
        subprocess.run(cmd, check=True)

def is_root_media(path: Path):
    return path.is_file() and path.parent.name not in SKIP_DIRS

def main():
    parser = argparse.ArgumentParser(
        description="Phase 4: finalize all photos and videos (UI + UI-less)"
    )
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()

    FINAL_PHOTOS.mkdir(exist_ok=True)
    FINAL_VIDEOS.mkdir(exist_ok=True)

    # ------------------------------------------------------------
    # PHOTOS
    # ------------------------------------------------------------
    print("[INFO] Finalizing photos")

    # UI photos
    if RENDERED_PHOTOS.exists():
        for img in RENDERED_PHOTOS.glob("*.jpg"):
            dest = FINAL_PHOTOS / img.name
            if not dest.exists():
                print(f"[PHOTO:UI] {img.name}")
                if not args.dry_run:
                    img.rename(dest)

    # UI-less photos
    for img in Path(".").glob("*.jpg"):
        if not is_root_media(img):
            continue
        dest = FINAL_PHOTOS / img.name
        if dest.exists():
            continue
        print(f"[PHOTO:UILess] {img.name}")
        if not args.dry_run:
            img.rename(dest)

    # ------------------------------------------------------------
    # VIDEOS
    # ------------------------------------------------------------
    print("[INFO] Finalizing videos")

    # UI videos (already reconstructed)
    if VIDEO_FIXED.exists():
        for vid in VIDEO_FIXED.glob("*.mp4"):
            dest = FINAL_VIDEOS / vid.name
            if not dest.exists():
                print(f"[VIDEO:UI] {vid.name}")
                if not args.dry_run:
                    vid.rename(dest)

    # UI-less videos
    for vid in Path(".").glob("*.mp4"):
        if not is_root_media(vid):
            continue
        dest = FINAL_VIDEOS / vid.name
        if dest.exists():
            continue
        print(f"[VIDEO:UILess] {vid.name}")
        if not args.dry_run:
            vid.rename(dest)

    print("\nDONE — Phase 4 complete")
    print(f"Photos → {FINAL_PHOTOS}")
    print(f"Videos → {FINAL_VIDEOS}")

if __name__ == "__main__":
    main()

