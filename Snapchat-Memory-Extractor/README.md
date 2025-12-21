# Snapchat Memories Processing Pipeline

This repository contains a multi-phase pipeline for processing Snapchat Memories exports into clean, metadata-correct photos and videos suitable for archival tools (e.g. Immich, Google Photos, etc.).

The pipeline handles:

- Photos with UI overlays (ZIP files)
- Photos without UI (extensionless JPEGs)
- Videos (`.mp4`, `.mov`, `.qt`)
- Metadata normalization (timestamps, GPS, creation dates)
- Final directory organization


## 📁 Directory Layout (Required)

Your directory structure **must** look like this before running any scripts:

```text
parent_folder/
├── mydata~XXXXXXXXXXXX/          # Snapchat data dump (HTML lives here)
│   └── html/
│       └── memories_history.html
│
└── Photos/                       # Working directory (run scripts here)
    ├── *.zip                     # Snapchat overlay media
    ├── *.mp4                     # Snapchat videos
    ├── *.mov                     # Snapchat videos
    ├── *.qt                      # Snapchat videos
    ├── <extensionless files>     # UI-less photos (JPEG without extension)
    ├── snapchat.py
    ├── snapchat_phase2.py
    ├── snapchat_phase3.py
    ├── snapchat_phase3_5.py
    └── snapchat_phase4.py
```

## ▶️ How to Run

All scripts **must be run from inside the `Photos/` directory**.




## 🧩 Pipeline Phases (Execution Order Matters)

Run the scripts **in order**, exactly once per phase unless otherwise noted.

| Phase | Script | Purpose |
|-----|------|------|
| Phase 1 | `snapchat.py` | Normalize UI-less photos (extensionless JPEGs), fix filenames |
| Phase 2 | `snapchat_phase2.py` | Extract photos from Snapchat ZIP overlays |
| Phase 3 | `snapchat_phase3.py` | Normalize raw Snapchat videos (no UI overlays) |
| Phase 3.5 | `snapchat_phase3_5.py` | Reconstruct captioned videos by combining video + overlay |
| Phase 4 | `snapchat_phase4.py` | Final organization into `final_photos/` and `final_videos/` |

⚠️ **Do not skip Phase 3.5** if your export contains captioned videos (UUID-named assets).




## 🕒 Metadata Handling (Important)

- Snapchat ZIP exports **do not preserve full video metadata**
- Captioned videos **must be re-encoded**, which inherently strips timestamps
- Phase 3.5 reconstructs video content
- Metadata is **repaired post-render** using ExifTool

### Guaranteed Metadata After Pipeline
- CreateDate
- TrackCreateDate
- MediaCreateDate
- Orientation / rotation
- Audio preserved (copied, not re-encoded)

### Notes
- No transcoding occurs *after* metadata repair
- Phase 4 **only moves files** and never rewrites metadata
- All final media is safe for ingestion into Immich, Apple Photos, Google Photos, etc.

