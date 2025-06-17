# BGR File Sorter 🗂️

This is an automated file sorting system written in Python by Bonna Reñosa.  
It monitors multiple folders and automatically moves files based on file type.

## ✅ Features

- Monitors multiple folders (listed in `sources.txt`)
- Auto-sorts by file type using `file_types.json`
- Auto-creates folders if missing
- Logs all actions in `sort_log.csv`
- Silent background mode with `run_silent.vbs`

## 🚀 Quick Start

1. Clone the repo
2. (Optional) Create a virtual environment
3. Install dependencies:

   ```bash
   pip install -r requirements.txt
4. Run with:

   ```bash
    python main.py

    Or just double-click run_sorter.bat
    Or run silently with run_silent.vbs

📁 Config
sources.txt: List of folders to monitor

file_types.json: File type to subfolder mapping

sort_log.csv: Logs of all sorting actions

📦 Requirements
Python 3.10+

watchdog (pip install watchdog)
