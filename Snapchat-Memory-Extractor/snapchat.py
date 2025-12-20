#!/usr/bin/env python3

import argparse
import re
import subprocess
import zipfile
from pathlib import Path
from datetime import datetime
from zoneinfo import ZoneInfo
from bs4 import BeautifulSoup

# ================= CONFIG =================

HTML_FILE = "../mydata~XXXXXXXXXX/html/memories_history.html"
MEDIA_DIR = Path(".")
TMP_DIR = Path("tmp")
OUT_DIR = Path("rendered")

LOCAL_TZ = ZoneInfo("America/Chicago")
UTC = ZoneInfo("UTC")

# =========================================

TMP_DIR.mkdir(exist_ok=True)
OUT_DIR.mkdir(exist_ok=True)

# ---------- Helpers ----------

def run(cmd, dry):
    if dry:
        print(" ".join(cmd))
    else:
        subprocess.run(cmd, check=True)

def utc_to_local(ts):
    ts = ts.replace(" UTC", "").strip()
    dt = datetime.strptime(ts, "%Y-%m-%d %H:%M:%S")
    return dt.replace(tzinfo=UTC).astimezone(LOCAL_TZ).strftime("%Y:%m:%d %H:%M:%S")

def find_zip_for_mid(mid):
    for z in MEDIA_DIR.glob("*.zip"):
        try:
            with zipfile.ZipFile(z) as zipf:
                for name in zipf.namelist():
                    if mid in name:
                        return z
        except zipfile.BadZipFile:
            continue
    return None

def is_ui_less_photo(path):
    if not path.is_file():
        return False
    if "." in path.name:
        return False
    try:
        out = subprocess.check_output(
            ["exiftool", "-q", "-FileType", str(path)],
            text=True
        )
        return "JPEG" in out
    except Exception:
        return False

# ---------- HTML Parsing ----------

def parse_html():
    with open(HTML_FILE, encoding="utf-8") as f:
        soup = BeautifulSoup(f, "html.parser")

    records = []

    for row in soup.find_all("tr"):
        cols = row.find_all("td")
        if len(cols) < 4:
            continue

        ts = cols[0].get_text(strip=True)
        media_type = cols[1].get_text(strip=True).lower()
        location = cols[2].get_text(strip=True)

        lat = lon = None
        m = re.search(r'(-?\d+\.\d+),\s*(-?\d+\.\d+)', location)
        if m:
            lat, lon = m.group(1), m.group(2)

        link = row.find("a", onclick=True)
        if not link:
            continue

        mid_match = re.search(r'mid=([A-F0-9\-]+)', link["onclick"])
        if not mid_match:
            continue

        records.append({
            "mid": mid_match.group(1),
            "type": media_type,
            "ts": utc_to_local(ts),
            "lat": lat,
            "lon": lon
        })

    print(f"[INFO] Parsed {len(records)} memories from HTML")
    return records

# ---------- Image Rendering ----------

def tag_image(path, record, dry):
    cmd = [
        "exiftool",
        f"-DateTimeOriginal={record['ts']}",
        f"-CreateDate={record['ts']}",
        "-overwrite_original",
        str(path)
    ]

    if record["lat"] and record["lon"]:
        cmd.extend([
            f"-GPSLatitude={record['lat']}",
            f"-GPSLongitude={record['lon']}",
            "-GPSLatitudeRef=N" if float(record["lat"]) >= 0 else "-GPSLatitudeRef=S",
            "-GPSLongitudeRef=E" if float(record["lon"]) >= 0 else "-GPSLongitudeRef=W"
        ])

    run(cmd, dry)

def render_zip_photo(record, dry):
    zip_path = find_zip_for_mid(record["mid"])
    if not zip_path:
        return False

    tmp = TMP_DIR / record["mid"]
    tmp.mkdir(parents=True, exist_ok=True)

    with zipfile.ZipFile(zip_path) as z:
        z.extractall(tmp)

    main = next(tmp.glob("*-main.jpg"), None)
    overlay = next(tmp.glob("*-overlay.png"), None)

    if not main:
        return False

    uuid = main.stem.replace("-main", "")
    out = OUT_DIR / f"{uuid}.jpg"

    if overlay:
        run([
            "ffmpeg", "-y",
            "-i", str(main),
            "-i", str(overlay),
            "-filter_complex", "overlay=0:0",
            str(out)
        ], dry)
    else:
        run(["cp", str(main), str(out)], dry)

    tag_image(out, record, dry)
    return True

def render_ui_less_photo(record, dry):
    for f in MEDIA_DIR.iterdir():
        if is_ui_less_photo(f):
            out = OUT_DIR / f"{f.name}.jpg"
            run(["cp", "--", str(f), str(out)], dry)
            tag_image(out, record, dry)
            return True
    return False

# ---------- Main ----------

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()

    records = parse_html()

    for r in records:
        if r["type"] != "image":
            continue

        if render_zip_photo(r, args.dry_run):
            continue

        render_ui_less_photo(r, args.dry_run)

    print("\nDONE — Phase 1 complete")

if __name__ == "__main__":
    main()

