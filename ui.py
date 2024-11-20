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
    create_date_time_selector(root, "Set Start Date and Time:", config.get("start_date", ""), "start")

    # Stop Date and Time Selector
    create_date_time_selector(root, "Set Stop Date and Time:", config.get("stop_date", ""), "stop")

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
    ttk.Button(root, text="Run Tasks", command=lambda: run_tasks(root, arc_dps_logs_var, gw2ei_var, top_stats_var), bootstyle="success").pack(pady=20)

def create_date_time_selector(root, label, default_date, prefix):
    ttk.Label(root, text=label, bootstyle="secondary").pack(pady=10)
    frame = ttk.Frame(root)
    frame.pack()

    date_var = StringVar(value=default_date or datetime.now().strftime("%Y-%m-%d"))
    ttk.Entry(frame, textvariable=date_var, width=15).grid(row=0, column=0, padx=5)

    hour_spin = ttk.Spinbox(frame, from_=0, to=23, width=3, bootstyle="dark")
    hour_spin.grid(row=0, column=1, padx=2)
    hour_spin.set("00")

    minute_spin = ttk.Spinbox(frame, from_=0, to=59, width=3, bootstyle="dark")
    minute_spin.grid(row=0, column=2, padx=2)
    minute_spin.set("00")

    second_spin = ttk.Spinbox(frame, from_=0, to=59, width=3, bootstyle="dark")
    second_spin.grid(row=0, column=3, padx=2)
    second_spin.set("00")

    return date_var, hour_spin, minute_spin, second_spin
