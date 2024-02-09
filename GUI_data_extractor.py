import tkinter as tk
from tkinter.scrolledtext import ScrolledText
from colorama import Fore, Style, init, deinit
import re

# Initialize colorama
init(autoreset=True)


def extract_values(text):
    patterns = {
        "auth_organization": r'\$session\.Cookies\.Add\(\(New-Object System\.Net\.Cookie\("auth_organization", "([^"]+)", "/", "([^"]+)"\)\)\)',
        "auth_session": r'\$session\.Cookies\.Add\(\(New-Object System\.Net\.Cookie\("auth_session", "([^"]+)", "/", "([^"]+)"\)\)\)',
        "referer": r'"referer"="([^"]+)"',
    }

    results = set()
    for key, pattern in patterns.items():
        matches = re.findall(pattern, text)
        for match in matches:
            if isinstance(match, tuple):
                result = f"{key}={match[0]}"
            else:
                result = f"{key}={match}"
            results.add(result)

    return results


def on_submit():
    text = text_input.get("1.0", tk.END)
    extracted_values = extract_values(text)

    result_window = tk.Toplevel(root)
    result_window.title("Results")

    result_text = ScrolledText(result_window, width=80, height=20)
    result_text.pack(padx=10, pady=10)

    # Insert extracted values
    for value in extracted_values:
        result_text.insert(tk.END, str(value) + "\n")

    # Apply syntax highlighting after inserting the results
    apply_syntax_highlighting_to_result(result_text)


def apply_syntax_highlighting_to_result(result_text):
    # Configure syntax highlighting tags for result_text
    result_text.tag_configure("property", foreground="darkcyan")
    result_text.tag_configure("value", foreground="blue")

    # Highlight each line in result_text
    current_index = "1.0"
    while True:
        line_start = result_text.index(f"{current_index} linestart")
        line_end = result_text.index(f"{current_index} lineend")
        line_text = result_text.get(line_start, line_end)

        # Assuming your result format might be "key=value", adjust as necessary
        regex = r"^([^=]+)=([^=]+)$"
        match = re.match(regex, line_text)
        if match:
            property_start = f"{line_start}+{match.start(1)}c"
            property_end = f"{line_start}+{match.end(1)}c"
            value_start = f"{line_start}+{match.start(2)}c"
            value_end = f"{line_start}+{match.end(2)}c"
            result_text.tag_add("property", property_start, property_end)
            result_text.tag_add("value", value_start, value_end)

        current_index = result_text.index(f"{line_end}+1c")
        if current_index == result_text.index(tk.END):
            break


def undo():
    try:
        text_input.edit_undo()
    except tk.TclError:
        pass


def redo():
    try:
        text_input.edit_redo()
    except tk.TclError:
        pass


root = tk.Tk()
root.title("Data Extractor")
print(f"{Fore.LIGHTCYAN_EX}'Data Extractor'{Style.RESET_ALL} {Fore.LIGHTGREEN_EX}Started!{Style.RESET_ALL}")

text_input = ScrolledText(root, width=80, height=20, undo=True)
text_input.pack(padx=10, pady=10)

submit_button = tk.Button(root, text="Process", command=on_submit)
submit_button.pack(pady=10)

# Menu bar
menu_bar = tk.Menu(root)
root.config(menu=menu_bar)

# File menu
file_menu = tk.Menu(menu_bar, tearoff=0)
menu_bar.add_cascade(label="File", menu=file_menu)
file_menu.add_command(label="Undo", command=undo, accelerator="Ctrl+Z")
file_menu.add_command(label="Redo", command=redo, accelerator="Ctrl+Y")
file_menu.add_separator()
file_menu.add_command(label="Exit", command=root.quit)

# Bind keyboard shortcuts for Undo and Redo
root.bind("<Control-z>", lambda event: undo())
root.bind("<Control-y>", lambda event: redo())

root.mainloop()

# Deinitialize colorama
deinit()
