#!/usr/bin/env python3
import argparse
import subprocess
from bs4 import BeautifulSoup
from datetime import datetime, timedelta
from pathlib import Path
import json

HTML_FILE = "../mydata~1766217532221/html/memories_history.html"
VIDEO_DIR = Path(".")
SKIP_DIRS = {"videos_rendered", "rendered", "tmp", "extracted_videos"}

TIME_WINDOW_SECONDS = 3


def run(cmd, dry):
    if dry:
        print(cmd)
    else:
        subprocess.run(cmd, shell=True, check=True)


def parse_datetime(text):
    return datetime.strptime(text.replace(" UTC", ""), "%Y-%m-%d %H:%M:%S")


def utc_to_cst(dt):
    return dt - timedelta(hours=6)


def parse_memories():
    soup = BeautifulSoup(open(HTML_FILE, encoding="utf-8"), "html.parser")
    rows = soup.find_all("tr")[1:]

    memories = []
    for r in rows:
        cols = r.find_all("td")
        if len(cols) < 3:
            continue
        if cols[1].text.strip() != "Video":
            continue

        dt = parse_datetime(cols[0].text.strip())
        loc = cols[2].text.strip()

        lat = lon = None
        if "Latitude" in loc:
            try:
                part = loc.split(":")[1]
                lat, lon = map(float, part.split(","))
            except Exception:
                pass

        memories.append({
            "utc": dt,
            "cst": utc_to_cst(dt),
            "lat": lat,
            "lon": lon
        })

    return memories


def get_video_creation_time(path):
    try:
        cmd = [
            "ffprobe", "-v", "quiet",
            "-print_format", "json",
            "-show_entries", "format_tags=creation_time",
            str(path)
        ]
        out = subprocess.check_output(cmd)
        data = json.loads(out)
        ts = data["format"]["tags"]["creation_time"]
        return datetime.fromisoformat(ts.replace("Z", ""))
    except Exception:
        return None


def index_local_videos():
    videos = []
    for p in VIDEO_DIR.iterdir():
        if p.suffix.lower() != ".mp4":
            continue
        if p.parent.name in SKIP_DIRS:
            continue

        ct = get_video_creation_time(p)
        if ct:
            videos.append((p, utc_to_cst(ct)))
    return videos


def match_video(mem, videos, used):
    best = None
    best_delta = None

    for path, ts in videos:
        if path in used:
            continue

        delta = abs((ts - mem["cst"]).total_seconds())
        if delta <= TIME_WINDOW_SECONDS:
            if best is None or delta < best_delta:
                best = path
                best_delta = delta

    return best


def process(mem, file, dry):
    dt = mem["cst"].strftime("%Y:%m:%d %H:%M:%S")

    cmd = [
        "exiftool",
        f'-CreateDate="{dt}"',
        f'-TrackCreateDate="{dt}"',
        "-overwrite_original"
    ]

    if mem["lat"] is not None and mem["lon"] is not None:
        cmd.append(f'-GPSCoordinates="{mem["lat"]},{mem["lon"]}"')

    cmd.append(str(file))
    run(" ".join(cmd), dry)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()

    memories = parse_memories()
    videos = index_local_videos()

    print(f"[INFO] Parsed {len(memories)} video memories from HTML")
    print(f"[INFO] Indexed {len(videos)} local MP4 files with embedded timestamps")

    used = set()
    matched = 0

    for mem in memories:
        f = match_video(mem, videos, used)
        if not f:
            continue

        print(f"[VIDEO] {f.name}")
        process(mem, f, args.dry_run)
        used.add(f)
        matched += 1

    print(f"\nDONE — matched {matched} videos")


if __name__ == "__main__":
    main()
