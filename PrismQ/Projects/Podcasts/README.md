# Podcasts Directory

This directory is for storing podcast audio files that will be published to Podbean.

## Usage

Place your generated podcast audio files here (e.g., `ep001.mp3`, `ep002.mp3`).

Example structure:
```
podcasts/
├── ep001.mp3
├── ep002.mp3
└── artwork/
    ├── ep001.jpg
    └── ep002.jpg
```

## Publishing

Use the GitHub Actions workflow "Publish to Podbean" or run the script directly:

```bash
export PODBEAN_CLIENT_ID="your_client_id"
export PODBEAN_CLIENT_SECRET="your_client_secret"
export AUDIO_PATH="podcasts/ep001.mp3"
export EP_TITLE="Episode 1: My First Episode"
export EP_DESC="This is the description for episode 1"

python scripts/publish_podbean.py
```
