import os
import tkinter as tk
from tkinter import ttk, filedialog
from datetime import datetime
import json

CONFIG_FILE = "config.json"

# Load saved config or default values
def load_config():
    if os.path.exists(CONFIG_FILE):
        try:
            with open(CONFIG_FILE, 'r') as f:
                return json.load(f)
        except Exception:
            pass
    return {"last_path": "", "elite_insights_path": "", "top_stats_path": ""}

# Save config to file
def save_config():
    with open(CONFIG_FILE, 'w') as f:
        json.dump(config, f)

config = load_config()

# Choose root folder
def choose_root_folder():
    folder = filedialog.askdirectory(title="Select Root Folder")
    if folder:
        for i in tree.get_children():
            tree.delete(i)
        checked_items.clear()
        populate_tree('', folder)
        config["last_path"] = folder
        save_config()
        selected_listbox.delete(0, tk.END)
        global root_path
        root_path = folder
        selected_path_label.config(text=f"Current Folder: {root_path}")

# Choose Elite Insights folder
def choose_elite_insights_path():
    path = filedialog.askdirectory(title="Select Elite Insights Folder")
    if path:
        config["elite_insights_path"] = path
        save_config()
        ei_path_label.config(text=f"Elite Insights Folder: {path}")

# Choose Top Stats Parser folder
def choose_top_stats_path():
    path = filedialog.askdirectory(title="Select Top Stats Parser Folder")
    if path:
        config["top_stats_path"] = path
        save_config()
        ts_path_label.config(text=f"Top Stats Parser Folder: {path}")

# Select all files modified after a certain date
def select_files_after_date():
    try:
        date_str = date_entry.get()
        cutoff = datetime.strptime(date_str, "%Y-%m-%d %H:%M")
        for item in tree.get_children(""):
            select_if_modified_after(item, cutoff)
        update_selected_list()
    except ValueError:
        print("Invalid date format. Use YYYY-MM-DD HH:MM")

def select_if_modified_after(item, cutoff):
    values = tree.item(item, "values")
    full_path = os.path.normpath(values[0]) if values else None  # Get the full path from the Treeview

    if full_path and os.path.isfile(full_path) and full_path.lower().endswith(".zevtc"):
        try:
            mod_time = datetime.fromtimestamp(os.path.getmtime(full_path))
            if mod_time > cutoff:
                checked_items[full_path] = True
                tree.item(item, text="✅ " + os.path.basename(full_path))
        except Exception as e:
            print(f"Error checking file: {e}")
    for child in tree.get_children(item):
        select_if_modified_after(child, cutoff)

# Unselect all

def unselect_all():
    for path in list(checked_items.keys()):
        del checked_items[path]
    for item in tree.get_children(""):
        clear_tree_checkboxes(item)
    update_selected_list()

def clear_tree_checkboxes(item):
    values = tree.item(item, "values")
    if values and values[0].lower().endswith(".zevtc"):
        tree.item(item, text=os.path.basename(values[0]))
    for child in tree.get_children(item):
        clear_tree_checkboxes(child)

# App window
root = tk.Tk()
root.title("GW2 arcdps File Selector")
root.geometry("1000x800")

# Elite Insights selector at top
ei_selector_frame = ttk.Frame(root)
ei_selector_frame.pack(fill="x", pady=5)

elite_button = ttk.Button(ei_selector_frame, text="Set Elite Insights Folder", command=choose_elite_insights_path)
elite_button.pack(side="left", padx=5)

ei_path_label = ttk.Label(ei_selector_frame, text=f"Elite Insights Folder: {config.get('elite_insights_path', '')}")
ei_path_label.pack(side="left", padx=10)

# Top Stats Parser selector below Elite Insights
ts_selector_frame = ttk.Frame(root)
ts_selector_frame.pack(fill="x", pady=5)

top_stats_button = ttk.Button(ts_selector_frame, text="Set Top Stats Parser Folder", command=choose_top_stats_path)
top_stats_button.pack(side="left", padx=5)

ts_path_label = ttk.Label(ts_selector_frame, text=f"Top Stats Parser Folder: {config.get('top_stats_path', '')}")
ts_path_label.pack(side="left", padx=10)

# Folder selector
top_frame = ttk.Frame(root)
top_frame.pack(fill="x")

select_folder_button = ttk.Button(top_frame, text="Select Folder", command=choose_root_folder)
select_folder_button.pack(side="left", padx=5, pady=5)

selected_path_label = ttk.Label(top_frame, text=f"Current Folder: {config.get('last_path', '')}")
selected_path_label.pack(side="left", padx=10)

# Main layout
main_frame = ttk.Frame(root)
main_frame.pack(fill="both", expand=True)
main_frame.rowconfigure(0, weight=1)
main_frame.columnconfigure(0, weight=1)

# Treeview container frame using grid
tree_frame = ttk.Frame(main_frame)
tree_frame.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)

# Treeview with checkboxes for file selection
tree = ttk.Treeview(tree_frame, columns=("modified",), selectmode="extended")
tree.heading("#0", text="File/Folder")
tree.heading("modified", text="Last Modified")
tree.column("modified", width=150)
tree.grid(row=0, column=0, sticky="nsew")

tree_frame.rowconfigure(0, weight=1)
tree_frame.columnconfigure(0, weight=1)

# Scrollbar for tree
tree_scroll = ttk.Scrollbar(tree_frame, orient="vertical", command=tree.yview)
tree.configure(yscrollcommand=tree_scroll.set)
tree_scroll.grid(row=0, column=1, sticky="ns")

# Filter by date section under tree
filter_frame = ttk.Frame(root)
filter_frame.pack(fill="x", pady=5)

date_label = ttk.Label(filter_frame, text="Select all logs modified after (YYYY-MM-DD HH:MM):")
date_label.pack(side="left", padx=5)

date_entry = ttk.Entry(filter_frame, width=20)
date_entry.pack(side="left")
date_entry.insert(0, datetime.now().strftime("%Y-%m-%d %H:%M"))

select_after_button = ttk.Button(filter_frame, text="Select Recent Logs", command=select_files_after_date)
select_after_button.pack(side="left", padx=10)

unselect_button = ttk.Button(filter_frame, text="Unselect All", command=unselect_all)
unselect_button.pack(side="left", padx=10)

# Listbox for selected files
selected_frame = ttk.Frame(main_frame)
selected_frame.grid(row=0, column=1, sticky="ns", padx=5, pady=5)

selected_label = ttk.Label(selected_frame, text="Selected .zevtc Files")
selected_label.pack(anchor="nw")

selected_listbox = tk.Listbox(selected_frame, width=60, selectmode="extended")
selected_listbox.pack(fill="y", expand=True)

count_label = ttk.Label(selected_frame, text="0 file(s) selected")
count_label.pack(anchor="nw", pady=(5, 0))

# Track selected files using checkboxes
tree.tag_configure("selected", background="#ccffcc")
checked_items = {}
root_path = config.get("last_path", "")

if root_path:
    selected_path_label.config(text=f"Current Folder: {root_path}")

last_selected = None

def update_selected_list():
    selected_listbox.delete(0, tk.END)
    count = 0
    for path in sorted(checked_items.keys()):
        display_name = os.path.relpath(path, root_path) if root_path else os.path.basename(path)
        selected_listbox.insert(tk.END, display_name)
        count += 1

    count_label.config(text=f"{count} file(s) selected")

    for item in tree.get_children(""):
        apply_tree_highlight(item)

def apply_tree_highlight(item):
    name = tree.item(item, "text").replace("✅ ", "")
    full_path = os.path.join(root_path, name)
    if full_path in checked_items:
        tree.item(item, tags=("selected",))
    else:
        tree.item(item, tags=())
    for child in tree.get_children(item):
        apply_tree_highlight(child)

def on_tree_click(event):
    global last_selected
    region = tree.identify("region", event.x, event.y)
    if region != "tree":
        return

    item_id = tree.identify_row(event.y)
    if not item_id:
        return

    values = tree.item(item_id, "values")
    if not values or not values[0].lower().endswith(".zevtc"):
        return

    full_path = os.path.normpath(values[0])  # Normalize the path

    if event.state & 0x0001 and last_selected:
        items = tree.get_children("")
        all_items = []
        def collect_items(i):
            all_items.append(i)
            for c in tree.get_children(i):
                collect_items(c)
        for i in items:
            collect_items(i)

        try:
            i1 = all_items.index(last_selected)
            i2 = all_items.index(item_id)
            for i in all_items[min(i1, i2):max(i1, i2)+1]:
                v = tree.item(i, "values")
                if v and v[0].lower().endswith(".zevtc"):
                    checked_items[os.path.normpath(v[0])] = True
                    tree.item(i, text="✅ " + os.path.basename(v[0]))
        except ValueError:
            pass
    else:
        if full_path in checked_items:
            del checked_items[full_path]
            tree.item(item_id, text=os.path.basename(full_path))
        else:
            checked_items[full_path] = True
            tree.item(item_id, text="✅ " + os.path.basename(full_path))
        last_selected = item_id

    update_selected_list()

def on_listbox_double_click(event):
    selection = selected_listbox.curselection()
    if selection:
        selected_name = selected_listbox.get(selection[0])
        full_path = os.path.join(root_path, selected_name)
        if full_path in checked_items:
            del checked_items[full_path]
            for item in tree.get_children(""):
                reset_tree_checkboxes(item, full_path)
            update_selected_list()

def reset_tree_checkboxes(item, full_path):
    values = tree.item(item, "values")
    if values and os.path.normpath(values[0]) == full_path:
        tree.item(item, text=os.path.basename(full_path))
        return True
    for child in tree.get_children(item):
        if reset_tree_checkboxes(child, full_path):
            return True
    return False

def populate_tree(parent, path):
    try:
        entries = sorted(os.listdir(path), key=lambda x: x.lower())
        for entry in entries:
            full_path = os.path.join(path, entry)  # Combine path and entry
            full_path = os.path.normpath(full_path)  # Normalize the full path
            if os.path.isdir(full_path):
                # Insert folder into the tree and recursively populate its children
                node = tree.insert(parent, "end", text=entry, values=(full_path,))  # Store full path for folders
                populate_tree(node, full_path)
            elif entry.lower().endswith(".zevtc"):
                # Insert file into the tree with its full path and modification time
                mod_time = datetime.fromtimestamp(os.path.getmtime(full_path)).strftime("%Y-%m-%d %H:%M")
                tree.insert(parent, "end", text=entry, values=(full_path, mod_time))  # Store full path for files
    except Exception as e:
        print(f"Error reading directory {path}: {e}")

if os.path.exists(root_path):
    populate_tree('', root_path)

tree.bind("<Button-1>", on_tree_click)
selected_listbox.bind("<Double-Button-1>", on_listbox_double_click)

root.mainloop()
