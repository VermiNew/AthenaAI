import tkinter as tk
from tkinter import messagebox
from tkinter.scrolledtext import ScrolledText
from colorama import Fore, Style, init, deinit
import re

# Initialize colorama
init(autoreset=True)

# Default file path
default_file_path = "data/config.ini"
filepath = ""


def open_file(filepath=None):
    if not filepath:
        # If no filepath is provided, use the default
        filepath = default_file_path
    text_area.delete(1.0, tk.END)
    with open(filepath, "r") as input_file:
        text = input_file.read()
        text_area.insert(tk.END, text)
    apply_syntax_highlighting()
    root.title(f"Syntax INI Editor - {filepath}")


def save_file(filepath=None):
    if not filepath:
        filepath = default_file_path
    with open(filepath, "w") as output_file:
        text = text_area.get(1.0, tk.END)
        output_file.write(text)
    root.title(f"Syntax INI Editor - {filepath}")
    messagebox.showinfo("Syntax INI Editor", "Saved successfully!")


def apply_syntax_highlighting(event=None):
    text_area.tag_remove("property", "1.0", tk.END)
    text_area.tag_remove("value", "1.0", tk.END)

    # Regex for properties and values
    regex = r"^([^=\s]+)\s*=\s*(.*)$"

    current_index = "1.0"
    while True:
        line_start = text_area.index(f"{current_index} linestart")
        line_end = text_area.index(f"{current_index} lineend")
        line_text = text_area.get(line_start, line_end)
        match = re.match(regex, line_text)
        if match:
            property_start = f"{line_start}+{match.start(1)}c"
            property_end = f"{line_start}+{match.end(1)}c"
            value_start = f"{line_start}+{match.start(2)}c"
            value_end = f"{line_start}+{match.end(2)}c"
            text_area.tag_add("property", property_start, property_end)
            text_area.tag_add("value", value_start, value_end)
        current_index = text_area.index(f"{line_end}+1c")
        if current_index == text_area.index(tk.END):
            break


def show_version():
    messagebox.showinfo("Version", "Syntax Highlighting INI Editor\nVersion 1.0")


def show_about():
    messagebox.showinfo(
        "What is this?", "This is a simple INI file editor with syntax highlighting."
    )


def undo():
    try:
        text_area.edit_undo()
    except tk.TclError:
        pass


def redo():
    try:
        text_area.edit_redo()
    except tk.TclError:
        pass


# Initialize tkinter
root = tk.Tk()
root.title("Syntax INI Editor - Select file")
print(
    f"{Fore.LIGHTCYAN_EX}'Config Editor'{Style.RESET_ALL} {Fore.LIGHTGREEN_EX}started!{Style.RESET_ALL}"
)

# Create Text Widget
text_area = ScrolledText(root, undo=True)
text_area.pack(expand=True, fill=tk.BOTH)
text_area.bind("<KeyRelease>", apply_syntax_highlighting)

# Keyboard shortcuts
root.bind("<Control-s>", lambda event: save_file(filepath))
root.bind("<Control-z>", lambda event: undo())
root.bind("<Control-y>", lambda event: redo())

# Menu bar
menu_bar = tk.Menu(root)
root.config(menu=menu_bar)

# File menu
file_menu = tk.Menu(menu_bar, tearoff=0)
menu_bar.add_cascade(label="File", menu=file_menu)
file_menu.add_command(label="Save", command=save_file, accelerator="Ctrl+S")
file_menu.add_command(label="Undo", command=undo, accelerator="Ctrl+Z")
file_menu.add_command(label="Redo", command=redo, accelerator="Ctrl+Y")
file_menu.add_separator()
file_menu.add_command(label="Exit", command=root.quit)

# Information menu
info_menu = tk.Menu(menu_bar, tearoff=0)
menu_bar.add_cascade(label="Informations", menu=info_menu)
info_menu.add_command(label="Version", command=show_version)
info_menu.add_command(label="What is this?", command=show_about)

# Syntax highlighting tags
text_area.tag_configure("property", foreground="gray")
text_area.tag_configure("value", foreground="blue")

# Open config.ini by default
open_file()

root.mainloop()

# Deinitialize colorama
deinit()
