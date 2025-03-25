import os
from utils import (
    load_config,
    save_config,
    log_progress,
    scan_and_move_files,
    clear_folder,
    run_batch_script,
    organize_tid_files,
    ensure_folder_exists,
)

from datetime import datetime
from tkinter import Toplevel, Text, Scrollbar, messagebox

def run_tasks(
    root,
    arc_dps_logs_var,
    gw2ei_var,
    top_stats_var,
    start_date_var,
    start_hour_spin,
    start_minute_spin,
    start_second_spin,
    stop_date_var,
    stop_hour_spin,
    stop_minute_spin,
    stop_second_spin,
):
    """Run tasks and save all configuration values."""
    # Load and save configuration
    config = load_config()
    config["arc_dps_logs"] = arc_dps_logs_var.get()
    config["gw2ei_path"] = gw2ei_var.get()
    config["top_stats_path"] = top_stats_var.get()
    config["start_date"] = start_date_var.get()
    config["start_time"] = f"{start_hour_spin.get()}:{start_minute_spin.get()}:{start_second_spin.get()}"
    config["stop_date"] = stop_date_var.get()
    config["stop_time"] = f"{stop_hour_spin.get()}:{stop_minute_spin.get()}:{stop_second_spin.get()}"
    save_config(config)

    # Prepare paths and times
    source_folder = config["arc_dps_logs"]
    target_folder = os.path.join(
        os.path.dirname(source_folder), "arcdps.ei_logs", "processed_logs"
    )
    ensure_folder_exists(target_folder)

    batch_path = os.path.join(config["top_stats_path"], "TW5_parsing_arc_top_stats.bat")
    gw2ei_path = config["gw2ei_path"]
    top_stats_path = config["top_stats_path"]

    start_datetime = datetime.strptime(
        f"{config['start_date']} {config['start_time']}", "%Y-%m-%d %H:%M:%S"
    )
    stop_datetime = datetime.strptime(
        f"{config['stop_date']} {config['stop_time']}", "%Y-%m-%d %H:%M:%S"
    )

    # Create progress window
    progress_window = Toplevel(root)
    progress_window.title("Progress")
    progress_window.geometry("500x400")
    progress_text = Text(progress_window, wrap="word")
    progress_text.pack(expand=True, fill="both", padx=10, pady=10)
    scroll = Scrollbar(progress_window, command=progress_text.yview)
    progress_text.configure(yscrollcommand=scroll.set)
    scroll.pack(side="right", fill="y")

    try:
        # Task steps
        log_progress(progress_text, "Clearing target folder...")
        clear_folder(target_folder)

        log_progress(progress_text, "Scanning and moving files...")
        scan_and_move_files(source_folder, target_folder, start_datetime, stop_datetime)

        log_progress(progress_text, "Running batch script...")
        run_batch_script(batch_path, target_folder, gw2ei_path, top_stats_path)

        log_progress(progress_text, "Organizing .tid files...")
        organize_tid_files(target_folder)

        log_progress(progress_text, "Tasks completed successfully!")

    except Exception as e:
        log_progress(progress_text, f"Error: {str(e)}")
        messagebox.showerror("Error", f"An error occurred: {str(e)}")
