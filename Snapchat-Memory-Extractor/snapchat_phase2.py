#!/usr/bin/env python3

import argparse
import subprocess
from pathlib import Path
from datetime import datetime
from zoneinfo import ZoneInfo
from bs4 import BeautifulSoup
import re

HTML_PATH = "../mydata~XXXXXXXXXXX/html/memories_history.html"

MEDIA_DIR = Path(".")
OUT_DIR = Path("videos_rendered")
OUT_DIR.mkdir(exist_ok=True)

UTC = ZoneInfo("UTC")
CST = ZoneInfo("America/Chicago")

VIDEO_EXTS = (".mp4", ".mov", ".qt")

# -----------------------------
# Helpers
# -----------------------------

def run(cmd, dry):
    if dry:
        print(" ".join(cmd))
    else:
        subprocess.run(cmd, check=True)

def parse_datetime(text):
    text = text.replace(" UTC", "").strip()
    return datetime.strptime(text, "%Y-%m-%d %H:%M:%S").replace(tzinfo=UTC).astimezone(CST)

# -----------------------------
# HTML Parsing
# -----------------------------

def parse_memories():
    with open(HTML_PATH, "r", encoding="utf-8") as f:
        soup = BeautifulSoup(f, "html.parser")

    memories = []

    for row in soup.find_all("tr"):
        cells = [c.get_text(strip=True) for c in row.find_all("td")]
        if not cells or "Video" not in cells:
            continue

        dt = None
        for c in cells:
            if re.match(r"\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}", c):
                dt = parse_datetime(c)
                break
        if not dt:
            continue

        lat = lon = None
        for c in cells:
            if re.match(r"-?\d+\.\d+", c):
                if lat is None:
                    lat = c
                elif lon is None:
                    lon = c
                    break

        link = row.find("a", onclick=True)
        if not link:
            continue

        m = re.search(r"mid=([A-F0-9-]{36})", link["onclick"])
        if not m:
            continue

        memories.append({
            "uuid": m.group(1),
            "datetime": dt,
            "lat": lat,
            "lon": lon
        })

    print(f"[INFO] Parsed {len(memories)} video memories")
    return memories

# -----------------------------
# Video Processing
# -----------------------------

def find_video(uuid):
    for ext in VIDEO_EXTS:
        p = MEDIA_DIR / f"{uuid}{ext}"
        if p.exists():
            return p
    return None

def process_video(mem, dry):
    uuid = mem["uuid"]
    src = find_video(uuid)
    if not src:
        print(f"[WARN] Missing video: {uuid}")
        return

    out = OUT_DIR / f"{uuid}.mp4"

    run([
        "ffmpeg", "-y",
        "-i", str(src),
        "-c:v", "copy",
        "-c:a", "copy",
        str(out)
    ], dry)

    ts = mem["datetime"].strftime("%Y:%m:%d %H:%M:%S")

    exif = [
        "exiftool",
        f"-CreateDate={ts}",
        f"-TrackCreateDate={ts}",
        f"-MediaCreateDate={ts}",
        "-overwrite_original"
    ]

    if mem["lat"] and mem["lon"]:
        exif.append(f"-GPSCoordinates={mem['lat']},{mem['lon']}")

    exif.append(str(out))
    run(exif, dry)

# -----------------------------
# Main
# -----------------------------

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()

    memories = parse_memories()

    for mem in memories:
        process_video(mem, args.dry_run)

    print("\nDONE — Phase 2 complete")

if __name__ == "__main__":
    main()

