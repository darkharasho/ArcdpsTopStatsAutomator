import os
import json

def log_progress(progress_text, message):
    """Log a message to the progress text widget."""
    if progress_text:
        progress_text.insert("end", message + "")
        progress_text.see("end")

import shutil
from datetime import datetime

CONFIG_FILE = "config.json"

def ensure_folder_exists(folder_path):
    """Ensure a folder exists, creating it if necessary."""
    os.makedirs(folder_path, exist_ok=True)

def scan_and_move_files(source_folder, target_folder, start_time, stop_time):
    """Scan subdirectories for .zetc files modified within the start and stop times and move them to the target folder."""
    # Ensure the base folder exists
    ensure_folder_exists(target_folder)
    for folder in os.listdir(source_folder):
        folder_path = os.path.normpath(os.path.join(source_folder, folder))
        if os.path.isdir(folder_path):
            ei_logs_subfolder = target_folder
            print(f"[DEBUG] Target folder set to: {ei_logs_subfolder}")
            ensure_folder_exists(ei_logs_subfolder)
            for item in os.listdir(folder_path):
                item_path = os.path.join(folder_path, item)
                if item.endswith('.zetc') and os.path.isfile(item_path):
                    file_mtime = datetime.fromtimestamp(os.path.getmtime(item_path))
                    if start_time <= file_mtime <= stop_time:
                        shutil.copy(item_path, os.path.join(ei_logs_subfolder, item))
    for folder in os.listdir(source_folder):
        folder_path = os.path.join(source_folder, folder)
        if os.path.isdir(folder_path):
            for item in os.listdir(folder_path):
                item_path = os.path.join(folder_path, item)
                if item.endswith('.zetc') and os.path.isfile(item_path):
                    file_mtime = datetime.fromtimestamp(os.path.getmtime(item_path))
                    if start_time <= file_mtime <= stop_time:
                        os.makedirs(target_folder, exist_ok=True)
                        shutil.copy(item_path, os.path.join(target_folder, item))

def clear_folder(folder_path):
    """Delete all content in the given folder."""
    for item in os.listdir(folder_path):
        item_path = os.path.join(folder_path, item)
        if os.path.isdir(item_path):
            shutil.rmtree(item_path)
        else:
            os.remove(item_path)

def run_batch_script(batch_path, target_folder, gw2ei_path, top_stats_folder):
    """Run the batch script for processing files."""
    command = f'"{batch_path}" "{target_folder}" "{gw2ei_path}" "{top_stats_folder}"'
    result = os.system(command)
    if result != 0:
        raise RuntimeError(f"Batch script failed with exit code {result}")

def organize_tid_files(target_folder):
    """Organize .tid files into a separate folder."""
    tid_files_dir = os.path.join(target_folder, "tid_files")
    os.makedirs(tid_files_dir, exist_ok=True)
    for tid_file in [f for f in os.listdir(target_folder) if f.endswith(".tid")]:
        shutil.move(os.path.join(target_folder, tid_file), os.path.join(tid_files_dir, tid_file))
    os.system(f'explorer "{tid_files_dir}"')

def load_config():
    """Load configuration from the JSON file."""
    if os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, "r") as f:
            return json.load(f)
    # Default config if file does not exist
    return {
        "arc_dps_logs": "",
        "gw2ei_path": "",
        "top_stats_path": "",
        "start_date": "",
        "start_time": "00:00:00",
        "stop_date": "",
        "stop_time": "23:59:59",
    }

def save_config(config):
    """Save configuration to the JSON file."""
    with open(CONFIG_FILE, "w") as f:
        json.dump(config, f, indent=4)

def browse_folder(variable, key):
    """Open a file dialog to select a folder and save it to the config."""
    from tkinter import filedialog

    folder = filedialog.askdirectory()
    if folder:
        variable.set(folder)
        config = load_config()
        config[key] = folder
        save_config(config)
