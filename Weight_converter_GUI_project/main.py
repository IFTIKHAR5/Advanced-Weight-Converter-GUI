 # main.py
import tkinter as tk
from gui import WeightConverterApp

def main():
    """Main entry point for the application"""
    root = tk.Tk()
    app = WeightConverterApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()