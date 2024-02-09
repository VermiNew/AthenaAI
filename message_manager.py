import json
from colorama import Fore, Style


class MessageManager:
    def __init__(self, file_path):
        """Initializes the MessageManager with a file path for storing messages."""
        self.file_path = file_path
        self.messages = self.load_messages()

    def add_message(self, interaction_id, sender, message, logger):
        """Adds a message to the history."""
        new_message = {
            "MessageID": interaction_id,
            "Details": {"Name": sender, "Message": message},
        }
        self.messages.append(new_message)
        logger.info(
            f"{Fore.LIGHTBLUE_EX}Message added:{Style.RESET_ALL} {self.format_message(new_message)}"
        )

    def save_messages(self):
        """Saves the message history to a JSON file."""
        with open(self.file_path, "w", encoding="utf-8") as file:
            json.dump(self.messages, file, ensure_ascii=False, indent=4)

    def load_messages(self):
        """Loads the message history from a JSON file. Returns an empty list if the file does not exist."""
        try:
            with open(self.file_path, "r", encoding="utf-8") as file:
                return json.load(file)
        except FileNotFoundError:
            return []

    def get_messages(self, logger):
        """
        Reads the message history from the JSON file and returns it as a list.
        """
        try:
            with open(self.file_path, "r", encoding="utf-8") as file:
                return json.load(file)
        except FileNotFoundError:
            logger.warning(
                f"{Fore.LIGHTYELLOW_EX}Message history file not found. Creating a new one.{Style.RESET_ALL}"
            )
            return []
        except json.JSONDecodeError:
            logger.error(
                f"{Fore.RED}Error decoding JSON. The file might be empty or corrupted.{Style.RESET_ALL}"
            )
            return []

    def format_message(self, message):
        """Formats a message for display. Assumes message structure has 'MessageID' and 'Details'."""
        details = message["Details"]
        return (
            f"{Fore.LIGHTCYAN_EX}ID:{Style.RESET_ALL} {Fore.CYAN}{message['MessageID']}{Style.RESET_ALL}, "
            f"{Fore.LIGHTCYAN_EX}Name:{Style.RESET_ALL} {Fore.CYAN}{details['Name']}{Style.RESET_ALL}, "
            f"{Fore.LIGHTCYAN_EX}Message:{Style.RESET_ALL} {Fore.CYAN}{details['Message']}{Style.RESET_ALL}"
        )
