from ui import create_ui
from ttkbootstrap import Window

def main():
    root = Window(themename="darkly")
    root.title("ArcDPS Logs Processor")
    root.geometry("600x800")
    create_ui(root)
    root.mainloop()

if __name__ == "__main__":
    main()
