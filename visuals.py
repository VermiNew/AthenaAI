import time
from colorama import Fore, Style
import curses


def processing_animation(event):
    """
    Displays a sophisticated processing animation (spinner) in the terminal.

    Parameters:
    - event (threading.Event): An event to control the start/stop of the animation.
    """
    spinner = ["|", "/", "-", "\\"]
    idx = 0

    print(f"{Fore.LIGHTGREEN_EX}Processing...", end="")
    while not event.is_set():
        # Display the spinner animation
        print(
            f"\r{Fore.LIGHTGREEN_EX}Processing...{Style.RESET_ALL} {Fore.LIGHTWHITE_EX}{spinner[idx % len(spinner)]}{Style.RESET_ALL}",
            end="",
        )
        idx += 1
        time.sleep(0.15)

    # Clear the line after finishing
    print("\r" + " " * 30 + "\r", end="")


def draw_logo(stdscr, initial_delay, line_colorize_delay, final_display_duration):
    # Define logo lines
    logo_lines = [
        "          __          ",
        "         .88.         ",
        "        .8888.        ",
        "       :888888.       ",
        "      . `888888.      ",
        "     .8. `888888.     ",
        "    .8`8. `888888.    ",
        "   .8' `8. `888888.   ",
        "  .8'   `8. `888888.  ",
        " .8'     `8. `888888. ",
        ".8'       `8. `888888.",
        "",
        "",
        "",
        "    ::: ::::::::::: :::    ::: :::::::::: ::::    :::     :::     ",
        "  :+: :+:   :+:     :+:    :+: :+:        :+:+:   :+:   :+: :+:   ",
        " +:+   +:+  +:+     +:+    +:+ +:+        :+:+:+  +:+  +:+   +:+  ",
        "+#++:++#++: +#+     +#++:++#++ +#++:++#   +#+ +:+ +#+ +#++:++#++: ",
        "+#+     +#+ +#+     +#+    +#+ +#+        +#+  +#+#+# +#+     +#+ ",
        "+#+     #+# #+#     #+#    #+# #+#        #+#   #+#+# #+#     #+# ",
        "###     ### ###     ###    ### ########## ###    #### ###     ### ",
    ]

    try:
        # Hide the cursor to enhance the visual presentation
        curses.curs_set(0)

        # Initialize color pairs
        if curses.has_colors():
            curses.init_pair(1, curses.COLOR_WHITE, curses.COLOR_BLACK)
            curses.init_pair(2, curses.COLOR_CYAN, curses.COLOR_BLACK)

        # Calculate the starting row to center the logo vertically
        height, width = stdscr.getmaxyx()
        start_row = (height // 2) - (len(logo_lines) // 2)

        # Initially draw the logo in white
        for i, line in enumerate(logo_lines):
            start_col = (width // 2) - (len(line) // 2)
            start_col = max(start_col, 0)
            stdscr.addstr(start_row + i, start_col, line, curses.color_pair(1))
        stdscr.refresh()

        # Wait before starting to colorize to blue
        time.sleep(initial_delay)

        # Colorize the logo to blue, line by line
        for i, line in enumerate(logo_lines):
            start_col = (width // 2) - (len(line) // 2)
            start_col = max(start_col, 0)
            stdscr.addstr(start_row + i, start_col, line, curses.color_pair(2))
            stdscr.refresh()
            time.sleep(line_colorize_delay)  # Delay between coloring each line

        # Wait a moment before clearing the screen
        time.sleep(final_display_duration)
        stdscr.clear()
        stdscr.refresh()
    except Exception as e:
        # Ensure the cursor is visible if an exception occurs
        curses.curs_set(1)
        curses.endwin()
        print(f"An error occurred while displaying the logo: {e}")
    finally:
        # Make sure the cursor is visible after the animation
        curses.curs_set(1)
        curses.endwin()


def start_animation(initial_delay, line_colorize_delay, final_display_duration, logger):
    logger.info(f"{Fore.LIGHTBLUE_EX}Displaying logo...{Style.RESET_ALL}")
    try:
        curses.wrapper(
            lambda stdscr: draw_logo(
                stdscr, initial_delay, line_colorize_delay, final_display_duration
            )
        )
    except Exception as e:
        logger.error(
            f"{Fore.RED}An error occured while trying to display logo: {e}{Style.RESET_ALL}"
        )
    logger.info(f"{Fore.GREEN}Done!{Style.RESET_ALL}")
