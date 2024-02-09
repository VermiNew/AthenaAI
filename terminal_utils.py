from colorama import Fore, Style
import sys
import shutil
import re


def print_line(symbol, width, color):
    """
    Prints a line of 'symbol' characters in a specified color. If 'width' is "full_width",
    the line length is the terminal's current width. If 'width' is an int value, the line length
    is 'width' characters. Otherwise, the line spans the full terminal width by default.

    Parameters:
    - symbol: A string representing the symbol to print.
    - width: Can be the string "full_width", an int specifying the desired line width,
             or None. If None or "full_width", uses full terminal width.
    - color: A string representing the color to apply to the line. This should
             be an ANSI color code or a colorama Fore attribute.
    """
    try:
        # Ensure the symbol is a string and not empty
        if not isinstance(symbol, str) or len(symbol) == 0:
            raise ValueError("Symbol must be a non-empty string.")

        # Get the current terminal width
        terminal_width = shutil.get_terminal_size().columns

        # Determine the line length
        if width == "full_width" or width is None:
            line_length = terminal_width
        elif isinstance(width, int) and width > 0:
            line_length = min(width, terminal_width)
        else:
            raise ValueError("Width must be 'full_width', a positive integer or None.")

        # Calculate the number of times the symbol should be repeated
        num_repeats = line_length // len(symbol) + (line_length % len(symbol) > 0)

        # Print the line with color, ensuring it doesn't exceed the desired line length
        print(
            f"{color}{(symbol * num_repeats)[:line_length]}{Style.RESET_ALL}", end="\n"
        )

    except Exception as e:
        # Assuming colorama's Fore for error coloring
        print(f"{Fore.RED}An error occurred: {e}")


def print_centered_text(text):
    """
    Prints the provided text centered on the screen, ignoring Colorama escape sequences.

    Parameters:
    - text: A string representing the text to be printed.
    """
    try:
        # Ensure the text is a string
        if not isinstance(text, str):
            raise ValueError("Text must be a string.")

        # Regex to match ANSI escape sequences
        ansi_escape_sequence = re.compile(r"\x1B[@-_][0-?]*[ -/]*[@-~]")

        # Strip Colorama/ANSI escape sequences for accurate length calculation
        text_without_ansi = ansi_escape_sequence.sub("", text)

        # Get the current terminal width
        terminal_width = shutil.get_terminal_size().columns

        # Calculate the starting position for the stripped text to be centered
        start_position = (terminal_width - len(text_without_ansi)) // 2

        # Ensure start_position is not negative
        start_position = max(start_position, 0)

        # Print the original text (with escape sequences) centered
        print(" " * start_position + text)

    except Exception as e:
        print(f"{Fore.RED}An error occurred: {e}{Style.RESET_ALL}")


def flush_screen_by_newlines(height):
    """
    Clears the terminal screen by printing newline characters.

    This function can either clear the entire terminal screen by printing
    enough newline characters based on the terminal's current height, or
    print a specified number of newline characters if an integer value is
    provided as an argument.

    Parameters:
    - height (int or str): If an integer is provided, the function will print
      that many newline characters. If the string "full_height" is provided or
      the parameter is left as default, the function will clear the entire
      terminal screen by printing newline characters equal to the terminal's
      current height.
    """
    if height == "full_height":
        # Get the current terminal height
        terminal_height = shutil.get_terminal_size().lines
        # Print newline characters to 'clear' the screen based on terminal height
        print("\n" * terminal_height)
    elif isinstance(height, int) and height > 0:
        # Print the specified number of newline characters
        print("\n" * height)
    else:
        raise ValueError("Height must be a positive integer or 'full_height'.")


def move_cursor(row, col):
    """
    Move the cursor to the specified row and column in the terminal.

    Parameters:
    - row (int): The row number (1-based).
    - col (int): The column number (1-based).
    """
    # Construct the ANSI escape code for moving the cursor
    escape_code = f"\033[{row};{col}H"
    # Output the escape code to move the cursor
    sys.stdout.write(escape_code)
    sys.stdout.flush()
