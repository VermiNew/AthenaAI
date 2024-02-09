from colorama import Fore, Style


def print_saved_messages(message_id, profile, message, sticky=False):
    """
    Print a message in the chat simulation format.

    Parameters:
    - profile: The name of the profile sending the message.
    - message: The message content.
    - sticky: Whether the message is sticky (default: False).
    """
    sticky_tag = f"{Fore.GREEN}Sticky{Fore.LIGHTBLACK_EX} " if sticky else ""
    if profile:
        print(
            f"{sticky_tag}{Fore.LIGHTBLACK_EX}[{message_id}]{Style.RESET_ALL} {Fore.LIGHTCYAN_EX}{profile}{Style.RESET_ALL} {Fore.LIGHTBLUE_EX}{message}{Style.RESET_ALL}"
        )
    else:
        print(
            f"{sticky_tag}{Fore.LIGHTBLACK_EX}[{message_id}]{Style.RESET_ALL} {Fore.LIGHTBLUE_EX}{message}{Style.RESET_ALL}"
        )
