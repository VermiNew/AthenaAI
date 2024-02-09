from colorama import Fore, Style


def highlight_quotes_in_text(
    text, default_color=Fore.LIGHTBLUE_EX, quote_color=Fore.LIGHTWHITE_EX
):
    new_text = ""
    in_quotes = False
    for char in text:
        if (char == '"' or char == "“") and not in_quotes:  # Start of quote
            in_quotes = True
            new_text += quote_color + char
        elif (char == '"' or char == "”") and in_quotes:  # End of quote
            in_quotes = False
            new_text += char + default_color
        else:
            if in_quotes:
                new_text += quote_color + char
            else:
                new_text += default_color + char
    if in_quotes:  # Ensure reset at the end if still in quotes
        new_text += Style.RESET_ALL
    # Reset color at the end of the processing
    new_text += Style.RESET_ALL

    return new_text
