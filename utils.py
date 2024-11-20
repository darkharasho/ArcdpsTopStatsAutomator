import os  # Fix added
import json
from tkinter import filedialog

CONFIG_FILE = "config.json"

def load_config():
    if os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, "r") as f:
            return json.load(f)
    return {}

def save_config(config):
    with open(CONFIG_FILE, "w") as f:
        json.dump(config, f)

def browse_folder(variable, key):
    folder = filedialog.askdirectory()
    if folder:
        variable.set(folder)
        config = load_config()
        config[key] = folder
        save_config(config)

def log_progress(progress_text, message):
    progress_text.insert("end", message + "\n")
    progress_text.see("end")

def execute_batch_command(progress_text, target_folder, gw2ei_path, top_stats_path):
    batch_command = f'"{top_stats_path}/TW5_parsing_arc_top_stats.bat" "{target_folder}" "{gw2ei_path}" "{top_stats_path}"'
    log_progress(progress_text, "Running batch command...")
    os.system(batch_command)
    log_progress(progress_text, "Batch command completed.")
