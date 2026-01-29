# MyCloud Storage (Telegram-Based)

## Overview
A Flask-based cloud storage system that uses **Telegram** as its unlimited backend storage.

## Features
1.  **Unlimited Storage**: Uses Telegram Channels to store files.
2.  **Chunking**: Splits large files (up to 20GB support logic) into 49MB chunks automatically.
3.  **Metadata Database**: Stores file info in a separate Metadata Channel (and caches in RAM).
4.  **Streaming Download**: Reconstructs files on-the-fly when downloading.

## Setup
1.  **Install Requirements**:
    ```bash
    pip install -r requirements.txt
    ```
2.  **Environment Variables** (`.env`):
    *   `TELEGRAM_BOT_TOKEN`
    *   `TELEGRAM_STORAGE_CHANNEL_ID`
    *   `TELEGRAM_METADATA_CHANNEL_ID`
    *   `SECRET_KEY`

## Running
```bash
python app.py
```
Visit `http://127.0.0.1:5000`

## Usage
1.  Login (Email based).
2.  Go to Dashboard.
3.  Upload File -> Watch progress.
4.  Download File -> Streams back to you.

## Notes
-   **Files are stored in RAM list (`FILES_DB`) for this MVP**. If you restart the server, the *list* resets, but the files are safe in Telegram. To restore the list, we would need to implement a "Scan Metadata Channel" feature (Step 10 extra credit).
