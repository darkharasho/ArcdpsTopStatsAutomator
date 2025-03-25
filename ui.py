import os
from datetime import datetime
from tkinter import StringVar
from ttkbootstrap import ttk
from ttkbootstrap.constants import *
from utils import load_config, browse_folder
from logic import run_tasks

def create_ui(root):
    config = load_config()

    # ArcDPS Logs Folder UI
    arc_dps_logs_var = StringVar(value=config.get("arc_dps_logs", ""))
    ttk.Label(root, text="Select ArcDPS Logs Folder:", bootstyle="secondary").pack(pady=5)
    ttk.Entry(root, textvariable=arc_dps_logs_var, width=60).pack(pady=5)
    ttk.Button(root, text="Browse", command=lambda: browse_folder(arc_dps_logs_var, "arc_dps_logs"), bootstyle="dark").pack(pady=5)

    # Start Date and Time Selector
    start_date_var, start_hour_spin, start_minute_spin, start_second_spin = create_date_time_selector(
        root,
        "Set Start Date and Time:",
        config.get("start_date", ""),
        config.get("start_time", ""),
        "start",
    )

    # Stop Date and Time Selector
    stop_date_var, stop_hour_spin, stop_minute_spin, stop_second_spin = create_date_time_selector(
        root,
        "Set Stop Date and Time:",
        config.get("stop_date", ""),
        config.get("stop_time", ""),
        "stop",
    )

    # GW2EI Path Selection
    gw2ei_var = StringVar(value=config.get("gw2ei_path", ""))
    ttk.Label(root, text="GW2EI Path:", bootstyle="secondary").pack(pady=5)
    ttk.Entry(root, textvariable=gw2ei_var, width=60, state="readonly").pack(pady=5)
    ttk.Button(root, text="Set GW2EI Path", command=lambda: browse_folder(gw2ei_var, "gw2ei_path"), bootstyle="dark").pack(pady=5)

    # Top Stats Parser Path Selection
    top_stats_var = StringVar(value=config.get("top_stats_path", ""))
    ttk.Label(root, text="Top Stats Parser Path:", bootstyle="secondary").pack(pady=5)
    ttk.Entry(root, textvariable=top_stats_var, width=60, state="readonly").pack(pady=5)
    ttk.Button(root, text="Set Top Stats Parser Path", command=lambda: browse_folder(top_stats_var, "top_stats_path"), bootstyle="dark").pack(pady=5)

    # Run Button
    ttk.Button(
        root,
        text="Run Tasks",
        command=lambda: run_tasks(
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
        ),
        bootstyle="success",
    ).pack(pady=20)

def create_date_time_selector(root, label, default_date, default_time, prefix):
    ttk.Label(root, text=label, bootstyle="secondary").pack(pady=10)
    frame = ttk.Frame(root)
    frame.pack()

    # Determine the date and time values
    today = datetime.now().strftime("%Y-%m-%d")
    date_value = default_date if default_date else today
    time_value = default_time if default_time else "00:00:00"
    print(f"[DEBUG] Setting default date for {prefix} to: {date_value}")
    print(f"[DEBUG] Setting default time for {prefix} to: {time_value}")

    # Create StringVar for date
    date_var = StringVar(value=date_value)
    ttk.Entry(frame, textvariable=date_var, width=15).grid(row=0, column=0, padx=5)

    # Split time into hours, minutes, and seconds
    hours, minutes, seconds = map(int, time_value.split(":"))

    # Create spinboxes for time
    hour_spin = ttk.Spinbox(frame, from_=0, to=23, width=3, bootstyle="dark")
    hour_spin.grid(row=0, column=1, padx=2)
    hour_spin.set(f"{hours:02}")

    minute_spin = ttk.Spinbox(frame, from_=0, to=59, width=3, bootstyle="dark")
    minute_spin.grid(row=0, column=2, padx=2)
    minute_spin.set(f"{minutes:02}")

    second_spin = ttk.Spinbox(frame, from_=0, to=59, width=3, bootstyle="dark")
    second_spin.grid(row=0, column=3, padx=2)
    second_spin.set(f"{seconds:02}")

    return date_var, hour_spin, minute_spin, second_spin

