import os  # Fix added
from datetime import datetime
from utils import log_progress, execute_batch_command

def run_tasks(root, arc_dps_logs_var, gw2ei_var, top_stats_var):
    # Get variables
    arc_dps_logs = arc_dps_logs_var.get()
    gw2ei_path = gw2ei_var.get()
    top_stats_path = top_stats_var.get()

    # Validate inputs
    if not arc_dps_logs or not gw2ei_path or not top_stats_path:
        messagebox.showerror("Error", "Please ensure all required paths are selected.")
        return

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
        # Example: File processing logic
        log_progress(progress_text, "Starting task...")
        target_folder = os.path.join(arc_dps_logs, "processed_logs")
        os.makedirs(target_folder, exist_ok=True)

        # Process files (add your file processing logic here)
        for file in os.listdir(arc_dps_logs):
            if file.endswith(".log"):
                shutil.copy(os.path.join(arc_dps_logs, file), target_folder)
                log_progress(progress_text, f"Copied: {file}")

        # Run batch command
        execute_batch_command(progress_text, target_folder, gw2ei_path, top_stats_path)

        # Open the folder with tid files
        tid_folder = os.path.join(target_folder, "tid_files")
        os.makedirs(tid_folder, exist_ok=True)
        os.system(f'explorer "{tid_folder}"')
        log_progress(progress_text, "Opened tid files folder.")

    except Exception as e:
        log_progress(progress_text, f"Error: {str(e)}")
