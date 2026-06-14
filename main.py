import tkinter as tk
from gui.GUICore import GUICore

def main():
    root = tk.Tk()
    launcher = GUICore(root)
    root.mainloop()

if __name__ == "__main__":
    main()