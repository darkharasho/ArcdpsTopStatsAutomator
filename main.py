import os
import json
import shutil
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from tkinter import filedialog, messagebox, Toplevel, Text, Scrollbar, END
from datetime import datetime
import threading

# File to save paths
CONFIG_FILE = "config.json"

# Load saved paths
def load_config():
    if os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, "r") as f:
            return json.load(f)
    return {"gw2ei_path": "", "top_stats_path": "", "arc_dps_logs": ""}

# Save paths
def save_config(config):
    with open(CONFIG_FILE, "w") as f:
        json.dump(config, f)

# Browse for a folder and update the corresponding variable
def browse_folder(variable, label):
    folder_selected = filedialog.askdirectory()
    if folder_selected:
        variable.set(folder_selected)
        config[label] = folder_selected
        save_config(config)

# Append messages to the progress window
def log_progress(progress_text, message):
    progress_text.insert(END, message + "\n")
    progress_text.see(END)

# Delete all content in the target folder
def delete_all_content(folder_path, progress_text):
    log_progress(progress_text, f"Clearing folder: {folder_path}")
    for item in os.listdir(folder_path):
        item_path = os.path.join(folder_path, item)
        if os.path.isdir(item_path):
            shutil.rmtree(item_path)
        else:
            os.remove(item_path)

# Combine date and time into a single string
def get_datetime(date_var, hour_spin, minute_spin, second_spin):
    return f"{date_var.get()} {hour_spin.get()}:{minute_spin.get()}:{second_spin.get()}"

# Perform the folder cleanup, file copying, and parsing tasks
def run_tasks_in_thread(progress_text):
    try:
        arc_dps_logs = arc_dps_logs_var.get()
        start_datetime_str = get_datetime(start_date_var, start_hour_spin, start_minute_spin, start_second_spin)
        stop_datetime_str = get_datetime(stop_date_var, stop_hour_spin, stop_minute_spin, stop_second_spin)
        gw2ei_path = gw2ei_var.get()
        top_stats_path = top_stats_var.get()
        target_folder = os.path.join(arc_dps_logs, "processed_logs")

        # Parse start and stop datetime
        start_datetime = datetime.strptime(start_datetime_str, "%Y-%m-%d %H:%M:%S")
        stop_datetime = datetime.strptime(stop_datetime_str, "%Y-%m-%d %H:%M:%S")

        # Step 1: Delete all content in the target folder
        os.makedirs(target_folder, exist_ok=True)
        delete_all_content(target_folder, progress_text)

        # Step 2: Copy files created within the start and stop times
        log_progress(progress_text, "Copying files created within the specified date and time range...")
        for folder in os.listdir(arc_dps_logs):
            folder_path = os.path.join(arc_dps_logs, folder)
            if os.path.isdir(folder_path):
                for item in os.listdir(folder_path):
                    item_path = os.path.join(folder_path, item)
                    target_file_path = os.path.join(target_folder, item)
                    if os.path.isfile(item_path):
                        # Get the file's last modified time
                        file_mtime = datetime.fromtimestamp(os.path.getmtime(item_path))
                        # Copy only if the file's mtime is within the start and stop times
                        if start_datetime <= file_mtime <= stop_datetime:
                            if not os.path.exists(target_file_path):  # Skip duplicates
                                shutil.copy(item_path, target_file_path)
                                log_progress(progress_text, f"Copied: {item}")
                            else:
                                log_progress(progress_text, f"Skipped duplicate: {item}")

        # Step 3: Run parsing commands
        log_progress(progress_text, "Running parsing batch command...")
        bash_command = f'"{top_stats_path}/TW5_parsing_arc_top_stats.bat" "{target_folder}" "{gw2ei_path}" "{top_stats_path}"'
        os.system(bash_command)
        log_progress(progress_text, "Parsing completed.")

        # Step 4: Move `.tid` files to a subdirectory
        log_progress(progress_text, "Organizing .tid files...")
        tid_folder = os.path.join(target_folder, "tid_files")
        os.makedirs(tid_folder, exist_ok=True)
        for tid_file in [f for f in os.listdir(target_folder) if f.endswith(".tid")]:
            shutil.move(os.path.join(target_folder, tid_file), os.path.join(tid_folder, tid_file))
            log_progress(progress_text, f"Moved: {tid_file}")

        # Step 5: Open the folder with `.tid` files
        log_progress(progress_text, "Opening folder with .tid files...")
        os.system(f'explorer "{tid_folder}"')
        log_progress(progress_text, "Tasks completed successfully!")
    except Exception as e:
        log_progress(progress_text, f"Error: {str(e)}")

# Launch a new thread for running tasks
def run_tasks():
    arc_dps_logs = arc_dps_logs_var.get()
    gw2ei_path = gw2ei_var.get()
    top_stats_path = top_stats_var.get()

    # Validate paths
    if not arc_dps_logs:
        messagebox.showerror("Error", "Please select the ArcDPS Logs Folder.")
        return
    if not gw2ei_path or not top_stats_path:
        messagebox.showerror("Error", "Please select paths for GW2EI and arcdps_top_stats_parser.")
        return

    # Progress Window
    progress_window = Toplevel(root)
    progress_window.title("Progress")
    progress_window.geometry("500x400")
    progress_text = Text(progress_window, wrap="word")
    progress_text.pack(expand=True, fill="both", padx=10, pady=10)
    scroll = Scrollbar(progress_window, command=progress_text.yview)
    progress_text.configure(yscrollcommand=scroll.set)
    scroll.pack(side="right", fill="y")

    # Run tasks in a separate thread
    threading.Thread(target=run_tasks_in_thread, args=(progress_text,), daemon=True).start()

# Main UI
config = load_config()
root = ttk.Window(themename="darkly")
root.title("ArcDPS Logs Processor")
root.geometry("600x800")

# ArcDPS Logs Folder UI
arc_dps_logs_var = ttk.StringVar(value=config.get("arc_dps_logs", ""))
ttk.Label(root, text="Select ArcDPS Logs Folder:", bootstyle="secondary").pack(pady=5)
ttk.Entry(root, textvariable=arc_dps_logs_var, width=60).pack(pady=5)
ttk.Button(root, text="Browse", command=lambda: browse_folder(arc_dps_logs_var, "arc_dps_logs"), bootstyle="dark").pack(pady=5)

# Start Date and Time Selector
ttk.Label(root, text="Set Start Date and Time:", bootstyle="secondary").pack(pady=10)
start_frame = ttk.Frame(root)
start_frame.pack()

start_date_var = ttk.StringVar(value=datetime.now().strftime("%Y-%m-%d"))
ttk.Entry(start_frame, textvariable=start_date_var, width=15).grid(row=0, column=0, padx=5)

start_hour_spin = ttk.Spinbox(start_frame, from_=0, to=23, width=3, bootstyle="dark")
start_hour_spin.grid(row=0, column=1, padx=2)
start_hour_spin.set("00")

start_minute_spin = ttk.Spinbox(start_frame, from_=0, to=59, width=3, bootstyle="dark")
start_minute_spin.grid(row=0, column=2, padx=2)
start_minute_spin.set("00")

start_second_spin = ttk.Spinbox(start_frame, from_=0, to=59, width=3, bootstyle="dark")
start_second_spin.grid(row=0, column=3, padx=2)
start_second_spin.set("00")

# Stop Date and Time Selector
ttk.Label(root, text="Set Stop Date and Time:", bootstyle="secondary").pack(pady=10)
stop_frame = ttk.Frame(root)
stop_frame.pack()

stop_date_var = ttk.StringVar(value=datetime.now().strftime("%Y-%m-%d"))
ttk.Entry(stop_frame, textvariable=stop_date_var, width=15).grid(row=0, column=0, padx=5)

stop_hour_spin = ttk.Spinbox(stop_frame, from_=0, to=23, width=3, bootstyle="dark")
stop_hour_spin.grid(row=0, column=1, padx=2)
stop_hour_spin.set("23")

stop_minute_spin = ttk.Spinbox(stop_frame, from_=0, to=59, width=3, bootstyle="dark")
stop_minute_spin.grid(row=0, column=2, padx=2)
stop_minute_spin.set("59")

stop_second_spin = ttk.Spinbox(stop_frame, from_=0, to=59, width=3, bootstyle="dark")
stop_second_spin.grid(row=0, column=3, padx=2)
stop_second_spin.set("59")

# GW2EI path selection
gw2ei_var = ttk.StringVar(value=config.get("gw2ei_path", ""))
ttk.Label(root, text="GW2EI Path:", bootstyle="secondary").pack(pady=5)
ttk.Entry(root, textvariable=gw2ei_var, width=60, state="readonly").pack(pady=5)
ttk.Button(root, text="Set GW2EI Path", command=lambda: browse_folder(gw2ei_var, "gw2ei_path"), bootstyle="dark").pack(pady=5)

# Top Stats Parser path selection
top_stats_var = ttk.StringVar(value=config.get("top_stats_path", ""))
ttk.Label(root, text="Top Stats Parser Path:", bootstyle="secondary").pack(pady=5)
ttk.Entry(root, textvariable=top_stats_var, width=60, state="readonly").pack(pady=5)
ttk.Button(root, text="Set Top Stats Parser Path", command=lambda: browse_folder(top_stats_var, "top_stats_path"), bootstyle="dark").pack(pady=5)

# Run button
ttk.Button(root, text="Run Tasks", command=run_tasks, bootstyle="success").pack(pady=20)

# Run the application
root.mainloop()
