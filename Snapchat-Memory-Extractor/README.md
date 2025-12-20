# Snapchat Memories Processing Pipeline

This repository contains a multi-phase pipeline for processing Snapchat Memories exports into clean, metadata-correct photos and videos suitable for archival tools (e.g. Immich, Google Photos, etc.).

The pipeline handles:

- Photos with UI overlays (ZIP files)
- Photos without UI (extensionless JPEGs)
- Videos (`.mp4`, `.mov`, `.qt`)
- Metadata normalization (timestamps, GPS, creation dates)
- Final directory organization

---

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
