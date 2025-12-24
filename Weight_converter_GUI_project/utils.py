# utils.py
"""
Utility functions for the weight converter
"""
import tkinter as tk
from tkinter import ttk, messagebox
import re

def validate_number(input_str: str) -> bool:
    """
    Validate if a string is a valid number
    """
    if input_str == "":
        return False
    
    pattern = r'^-?\d*\.?\d+$'
    return bool(re.match(pattern, input_str))

def validate_positive_number(input_str: str) -> bool:
    """
    Validate if a string is a valid positive number
    """
    if not validate_number(input_str):
        return False
    
    try:
        value = float(input_str)
        return value >= 0
    except ValueError:
        return False

def show_error(message: str, parent=None):
    """
    Display an error message box
    """
    messagebox.showerror("Error", message, parent=parent)

def show_info(message: str, parent=None):
    """
    Display an info message box
    """
    messagebox.showinfo("Information", message, parent=parent)

def copy_to_clipboard(text: str, parent=None):
    """
    Copy text to clipboard and show confirmation
    """
    root = parent if parent else tk.Tk()
    root.clipboard_clear()
    root.clipboard_append(text)
    root.update()
    show_info("Results copied to clipboard!", parent)

def create_tooltip(widget, text):
    """
    Create a tooltip for a widget
    """
    tooltip = None
    
    def show_tooltip(event):
        nonlocal tooltip
        x, y, _, _ = widget.bbox("insert")
        x += widget.winfo_rootx() + 25
        y += widget.winfo_rooty() + 20
        
        tooltip = tk.Toplevel(widget)
        tooltip.wm_overrideredirect(True)
        tooltip.wm_geometry(f"+{x}+{y}")
        
        label = tk.Label(tooltip, text=text, justify='left',
                        background="#ffffe0", relief='solid', borderwidth=1,
                        font=("tahoma", "8", "normal"))
        label.pack()
    
    def hide_tooltip(event):
        nonlocal tooltip
        if tooltip:
            tooltip.destroy()
            tooltip = None
    
    widget.bind('<Enter>', show_tooltip)
    widget.bind('<Leave>', hide_tooltip)

def apply_theme(root, theme='light'):
    """
    Apply a theme to the application
    """
    if theme == 'dark':
        bg_color = '#2b2b2b'
        fg_color = '#ffffff'
        entry_bg = '#3c3f41'
        button_bg = '#4e5254'
        frame_bg = '#3c3f41'
        label_bg = '#2b2b2b'
    else:
        bg_color = '#f0f0f0'
        fg_color = '#000000'
        entry_bg = '#ffffff'
        button_bg = '#e0e0e0'
        frame_bg = '#ffffff'
        label_bg = '#f0f0f0'
    
    root.configure(bg=bg_color)
    
    def apply_to_widgets(widget):
        widget_type = widget.winfo_class()
        
        if widget_type in ('TFrame', 'Frame', 'Labelframe'):
            widget.configure(bg=frame_bg)
        elif widget_type in ('TLabel', 'Label'):
            widget.configure(bg=label_bg, fg=fg_color)
        elif widget_type in ('TEntry', 'Entry'):
            widget.configure(bg=entry_bg, fg=fg_color, insertbackground=fg_color)
        elif widget_type in ('TButton', 'Button'):
            widget.configure(bg=button_bg, fg=fg_color)
        elif widget_type in ('TCheckbutton', 'Checkbutton'):
            widget.configure(bg=label_bg, fg=fg_color)
        
        for child in widget.winfo_children():
            apply_to_widgets(child)
    
    apply_to_widgets(root)
    return theme