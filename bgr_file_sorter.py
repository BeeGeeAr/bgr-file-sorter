import os
import time
import json
import shutil
import csv
from datetime import datetime
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

SOURCES_FILE = "sources.txt"
TYPES_FILE = "file_types.json"
LOG_FILE = "sort_log.csv"

# Default content if config files are missing
DEFAULT_SOURCE_FOLDERS = [
    r"C:\\Users\\BGR\\Downloads",
    r"C:\\Users\\BGR\\Desktop"
]

DEFAULT_FILE_TYPE_MAP = {
    ".txt": "Text Files",
    ".pdf": "PDFs",
    ".jpg": "Images",
    ".png": "Images",
    ".xlsx": "Excel Files",
    ".docx": "Word Documents",
    ".pptx": "PowerPoint Presentations",
    ".mp4": "Video",
    ".mp3": "Audio Files",
    ".zip": "Compressed",
    ".py": "Python Files"
}

# Ensure sources.txt exists
def ensure_sources_file():
    if not os.path.exists(SOURCES_FILE):
        with open(SOURCES_FILE, "w", encoding="utf-8") as f:
            for path in DEFAULT_SOURCE_FOLDERS:
                f.write(f"{path}\n")
        print(f"🆕 Created default '{SOURCES_FILE}'")

# Ensure file_types.json exists
def ensure_file_type_map():
    if not os.path.exists(TYPES_FILE):
        with open(TYPES_FILE, "w", encoding="utf-8") as f:
            json.dump(DEFAULT_FILE_TYPE_MAP, f, indent=2)
        print(f"🆕 Created default '{TYPES_FILE}'")

# Ensure sort_log.csv exists with headers
def ensure_log_file():
    if not os.path.exists(LOG_FILE):
        with open(LOG_FILE, "w", newline="", encoding="utf-8") as log:
            writer = csv.writer(log)
            writer.writerow(["Timestamp", "Status", "Source", "Destination", "Extension"])

# Load source folders from text file
def load_source_folders():
    with open(SOURCES_FILE, "r", encoding="utf-8") as f:
        return [line.strip() for line in f if line.strip() and not line.startswith("#")]

# Load extension-to-folder map from JSON
def load_file_type_map():
    with open(TYPES_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

# Write a log entry
def log_action(status, src, dest, ext):
    with open(LOG_FILE, "a", newline="", encoding="utf-8") as log:
        writer = csv.writer(log)
        writer.writerow([
            datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            status,
            src,
            dest,
            ext
        ])

# Custom file watcher handler
class FileSorterHandler(FileSystemEventHandler):
    def __init__(self, source_folder, file_type_map):
        super().__init__()
        self.source_folder = source_folder
        self.file_type_map = file_type_map

    def on_created(self, event):
        if not event.is_directory:
            file_path = event.src_path
            _, ext = os.path.splitext(file_path)
            ext = ext.lower()
            subfolder = self.file_type_map.get(ext)

            if subfolder:
                destination_folder = os.path.join(self.source_folder, subfolder)
                os.makedirs(destination_folder, exist_ok=True)
                try:
                    filename = os.path.basename(file_path)
                    new_path = os.path.join(destination_folder, filename)
                    shutil.move(file_path, new_path)
                    print(f"✅ Moved: {filename} → {destination_folder}")
                    log_action("Moved", file_path, new_path, ext)
                except Exception as e:
                    print(f"❌ Error moving {file_path}: {e}")
                    log_action(f"Error: {e}", file_path, "", ext)
            else:
                print(f"⚠️ No rule for file type: {ext} (file: {file_path})")
                log_action("Skipped (no rule)", file_path, "", ext)

# Main runner
if __name__ == "__main__":
    ensure_sources_file()
    ensure_file_type_map()
    ensure_log_file()

    source_folders = load_source_folders()
    file_type_map = load_file_type_map()
    observers = []

    for folder in source_folders:
        if not os.path.exists(folder):
            print(f"⚠️ Skipped missing folder: {folder}")
            continue

        print(f"🚀 Watching: {folder}")
        handler = FileSorterHandler(folder, file_type_map)
        observer = Observer()
        observer.schedule(handler, folder, recursive=False)
        observer.start()
        observers.append(observer)

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        for observer in observers:
            observer.stop()
        for observer in observers:
            observer.join()
