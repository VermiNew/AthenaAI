from colorama import Fore, Style, init
import json
from pygments import highlight, lexers, formatters
import threading
from rich.console import Console
from rich.traceback import install
import logging
from config_loader import load_config, get_config_info
from config_data import (
    generate_data,
    load_credentials,
    format_filtered_word,
    print_credentials,
)
from session_manager import setup_session, post_event, post_stateful
from json_parser import (
    parse_jsons,
    combine_json_objects,
    extract_from_json,
    remove_word_from_list,
)
from text_colorizer import highlight_quotes_in_text
from text_processing import (
    print_message_word_by_word,
    process_json_response,
    is_input_well_formed,
)
from visuals import processing_animation, start_animation
from input_validation import get_user_confirmation
from terminal_utils import (
    print_line,
    print_centered_text,
    flush_screen_by_newlines,
    move_cursor,
)
from backup_controller import (
    update_interactions,
    start_background_saving,
    register_signal_handlers,
    register_exit_handler,
)
import time
from cleanup import PyCacheCleaner
from chat_loader import print_saved_messages
from message_manager import MessageManager

install()
console = Console()
init(autoreset=True)


def setup_logger(log_path):
    """Set up the logger for the application."""
    # Create a logger
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.DEBUG)  # Set the minimum log level to DEBUG

    # Create a file handler for writing logs to a file
    file_handler = logging.FileHandler(log_path)
    file_handler.setLevel(logging.DEBUG)  # Set the minimum log level for the file

    # Create a console handler for outputting logs to the console
    console_handler = logging.StreamHandler()
    console_handler.setLevel(
        logging.WARNING
    )  # Set the minimum log level for the console

    # Create a formatter and set it for both handlers
    Fformatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )
    Cformatter = logging.Formatter(
        f"{Fore.LIGHTBLACK_EX}<%(levelname)s>:{Style.RESET_ALL} %(message)s"
    )
    file_handler.setFormatter(Fformatter)
    console_handler.setFormatter(Cformatter)

    # Add the handlers to the logger
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)

    return logger


class Chatbot:
    def __init__(self):
        self.config_path = "data/config.ini"
        self.backup_path = "data/backup.json"
        self.history_path = "conv/messages_history.json"
        self.interactions = 8
        self.backup_interval = 3600  # For example, save every hour
        self.log_path = "chatbot.log"
        self.logger = setup_logger(self.log_path)
        self.logger.info(
            f"{Fore.GREEN}Chatbot instance has been created{Style.RESET_ALL}"
        )

    def run(self):
        # Loads config
        self.logger.info(
            f"{Fore.LIGHTBLUE_EX}Config path set to:{Style.RESET_ALL} {Fore.LIGHTCYAN_EX}'{self.config_path}'{Style.RESET_ALL}"
        )
        config = load_config(self.config_path, self.logger)

        # Setup session
        session = setup_session(config, self.logger)

        # Define backup path
        self.logger.info(
            f"{Fore.LIGHTBLUE_EX}Backup path set to:{Style.RESET_ALL} {Fore.LIGHTCYAN_EX}'{self.backup_path}'{Style.RESET_ALL}"
        )

        # Interactions
        self.interactions = get_user_confirmation(
            self.backup_path, self.interactions, self.logger
        )

        # Overwrite the interactions value
        update_interactions(self.interactions, self.logger)

        # Get name from credentials
        credentials = load_credentials(config)

        # Make filtered word
        filtered_word = format_filtered_word(credentials)
        self.logger.info(
            f"{Fore.LIGHTBLUE_EX}Filtered word set to: {Fore.CYAN}{filtered_word}"
        )

        # Print credentials
        print_credentials(config)

        # Get user informations
        userName = get_config_info(config, self.logger, "Credentials", "name")

        # Get model informations
        modelID = get_config_info(config, self.logger, "MODEL", "modelId")
        characterName = get_config_info(
            config, self.logger, "CHARACTER", "characterName"
        )
        self.logger.info(
            f"{Fore.LIGHTBLUE_EX}ModelID set to: {Fore.CYAN}{modelID}{Style.RESET_ALL}"
        )
        self.logger.info(
            f"{Fore.LIGHTBLUE_EX}CharacterName set to: {Fore.CYAN}{characterName}{Style.RESET_ALL}"
        )

        # Initialize backup process
        start_background_saving(self.backup_interval, self.backup_path, self.logger)
        register_signal_handlers(self.backup_path, self.logger)
        register_exit_handler(self.backup_path, self.logger)

        # Show AI config
        _, data_stateful, _ = generate_data(config, "", self.interactions)
        ai_configuration = extract_from_json(data_stateful, "samplingParams")
        self.logger.debug(ai_configuration)
        json_string = json.dumps(ai_configuration, indent=4)

        # Colorize the JSON output
        colorized_json = highlight(
            json_string, lexers.JsonLexer(), formatters.TerminalFormatter()
        )

        # Show model parameters
        print(
            f"{Fore.LIGHTMAGENTA_EX}Model Parameters:{Style.RESET_ALL}\n",
            colorized_json,
        )

        # Start the animation.
        start_animation(0.5, 0.05, 0.5, self.logger)

        # Clear screen leaving buffer
        flush_screen_by_newlines("full_height")

        # Move cursor
        move_cursor(0, 0)

        # Drawing interface informations
        print_line("-", "full_width", Fore.LIGHTBLACK_EX)
        print_centered_text(
            f"Selected model: {Fore.LIGHTYELLOW_EX}{modelID}{Style.RESET_ALL}, Simulating {Fore.CYAN}{characterName}{Style.RESET_ALL}'s character..."
        )
        print_line("-", "full_width", Fore.LIGHTBLACK_EX)
        time.sleep(0.5)
        print()

        print_centered_text(f"{Fore.LIGHTGREEN_EX}Model ready!{Style.RESET_ALL}")
        print()

        # Messages
        messages = [
            (
                "[Kiriko > HIDDEN]:",
                f"""[IMPORTANT]
INSTRUCTIONS:
1. Color Selection: AI dynamically selects colors from a predefined palette, ensuring readability.
Palette: (Fore.LIGHTRED_EX, Fore.LIGHTBLUE_EX, Fore.LIGHTGREEN_EX, Fore.YELLOW_EX, Fore.MAGENTA_EX, Fore.CYAN_EX, Fore.BLACK_EX)

2. Message Clarity: Messages are short, clear, jargon-free, and well-structured.

3. Formatting Restrictions: Do not use <instruction </instruction tags (even without closing) in any part of the communication.
Avoid using text fields in communication. Any additional information or narratives should be directly included in the message content.
Narration Instructions:
If you need to add extra information or describe a situation, use a narrative form, introducing it with "\n> Narrator:" at the end of your message.

4. AI Labeling in Communication: All AI-generated messages should be preceded by the label [Kiriko]: to clearly indicate they come from you.

5. User Interaction: AI encourages dialogue, asks for clarifications in case of misunderstandings.

6. User Feedback: AI adjusts responses based on feedback.

7. Do not use [{userName}] tag.""",
                True,
            ),
            (
                "[Kiriko]:",
                f"“Oh, {userName}, come on in. I'm glad you could make it.”",
                True,
            ),
            (
                "[User]:",
                "*nervously* “Um, thanks Kiriko. Your place is really nice.”",
                True,
            ),
            (
                "[Kiriko]:",
                f"""> Narrator: \"*Kiriko smiles warmly, sensing {userName}'s shyness, and gestures for him to take a seat on the sofa.*\"""",
                True,
            ),
            (
                "[Kiriko]:",
                "“Make yourself comfortable. Would you like some tea?”",
                True,
            ),
            (
                "[User]:",
                "Yes, please.",
                True,
            ),
            (
                "[Kiriko]:",
                f"""> Narrator: \"As {userName} settles into the sofa, Kiriko heads to the kitchen to prepare the tea. The room is cozy, filled with soft lighting and comfortable furniture, making it easy for {userName} to relax.\"""",
                True,
            ),
            (
                "[Kiriko]:",
                f"""> Narrator: \"Kiriko nods and decides on a calming herbal blend. Returning with two steaming cups, she places one in front of {userName} and sits down across from him, the warmth from the tea filling the space between them.\"""",
                True,
            ),
        ]

        # Print messages
        for profile, message, sticky in messages:
            message = highlight_quotes_in_text(message)
            print_saved_messages(0, profile, message, sticky)

        # Create an instance of MessageManager
        message_manager = MessageManager(self.history_path)

        messages = message_manager.get_messages(self.logger)
        for message in messages:  # Iterate directly over the list
            message_id = message[
                "MessageID"
            ]  # Adjusted according to your JSON structure
            details = message["Details"]  # Adjusted according to your JSON structure
            profile = details["Name"]
            message_text = details["Message"]
            message_text = highlight_quotes_in_text(message_text)
            print_saved_messages(message_id, profile, message_text, False)
        self.logger.info(f"{Fore.LIGHTCYAN_EX}Printing completed!{Style.RESET_ALL}")

        self.interactive_session(
            session, config, filtered_word, message_manager, userName
        )

    def interactive_session(
        self, session, config, filtered_word, message_manager, userName
    ):
        print_centered_text(
            f"{Fore.LIGHTBLACK_EX}Use {Fore.MAGENTA}!exit{Fore.LIGHTBLACK_EX} command to exit.{Style.RESET_ALL}"
        )
        while True:
            try:
                input_sentence = input(
                    f"{Fore.LIGHTGREEN_EX}[User]:{Fore.LIGHTYELLOW_EX} "
                )

                input_sentence = input_sentence.strip()
                well_formed_status = is_input_well_formed(input_sentence, self.logger)

                if input_sentence == "!exit":
                    self.logger.info(
                        f"{Fore.LIGHTBLUE_EX}Exit command used, exiting main loop...{Style.RESET_ALL}"
                    )
                    break
                elif input_sentence is None or input_sentence == "":
                    print_centered_text(
                        f"{Fore.RED}Please provide text!{Style.RESET_ALL}"
                    )
                    continue
                elif not well_formed_status:
                    print_centered_text(
                        f"{Fore.YELLOW}Kindly adjust the formatting of the submitted text accordingly.{Style.RESET_ALL}"
                    )
                    continue
                else:
                    self.logger.info(
                        f"{Fore.GREEN}Input message is okay.{Style.RESET_ALL}"
                    )

                self.interactions += 1
                update_interactions(self.interactions, self.logger)
                message_manager.add_message(
                    self.interactions, "[User]:", input_sentence, self.logger
                )
                self.logger.info(
                    f"{Fore.LIGHTCYAN_EX}Interactions value changed to: {self.interactions}{Style.RESET_ALL}"
                )

                # Generate data
                data_event, data_stateful, status = generate_data(
                    config, input_sentence, self.interactions
                )
                if status == 0:
                    self.logger.info(
                        f"{Fore.LIGHTMAGENTA_EX}Status:{Style.RESET_ALL} {Fore.GREEN}{status}{Style.RESET_ALL}"
                    )
                else:
                    self.logger.info(
                        f"{Fore.RED}An error occurred!{Style.RESET_ALL} {Fore.LIGHTMAGENTA_EX}Status:{Style.RESET_ALL} {Fore.RED}{status}{Style.RESET_ALL}"
                    )
                    continue

                # Function to be called by the Timer after 15 seconds
                def stop_animation_after_timeout():
                    if not stop_animation.is_set():
                        self.logger.warning(
                            f"{Fore.LIGHTYELLOW_EX}Warning: Animation timed out after 15 seconds.{Style.RESET_ALL}"
                        )
                        stop_animation.set()

                # Create an event object
                stop_animation = threading.Event()

                # Start the processing animation in a separate thread
                animation_thread = threading.Thread(
                    target=processing_animation, args=(stop_animation,)
                )
                animation_thread.start()

                # Start a timer for 15 seconds that will stop the animation if it's still running
                timeout_timer = threading.Timer(15, stop_animation_after_timeout)
                timeout_timer.start()

                # Post data
                try:
                    response_event = post_event(
                        session, config, data_event, self.logger
                    )
                    if response_event is None:
                        self.logger.debug(
                            f"{Fore.RED}A serious error occurred.{Style.RESET_ALL}"
                        )
                    response_event.raise_for_status()  # Check for HTTP errors

                    if response_event and response_event.status_code == 200:
                        self.logger.debug(
                            f"{Fore.GREEN}Event posted successfully: {response_event.text}{Style.RESET_ALL}"
                        )
                    else:
                        if response_event.status_code == 202:
                            self.logger.debug(
                                f"{Fore.BLUE}Request accepted, but processing has not been completed. Checking status...{Style.RESET_ALL}"
                            )
                            # Implementacja mechanizmu odpytywania (polling)
                            while True:
                                status_response = post_event(
                                    session, config, data_event, self.logger
                                )
                                if status_response.status_code == 200:
                                    self.logger.debug(
                                        f"{Fore.GREEN}Processing completed.{Style.RESET_ALL}"
                                    )
                                    break
                                elif status_response.status_code == 202:
                                    self.logger.debug(
                                        f"{Fore.GREEN}Hey, even though I'm getting a 202 status on the event, I'm still moving forward to the main function.{Style.RESET_ALL}"
                                    )
                                    break
                                else:
                                    self.logger.debug(
                                        f"{Fore.RED}Failed to check status. Trying again...{Style.RESET_ALL}"
                                    )
                                    pass
                        else:
                            self.logger.debug(
                                f"{Fore.RED}Failed to post event. Status code: {response_event.status_code if response_event else 'N/A'}{Style.RESET_ALL}"
                            )

                    response_stateful = post_stateful(
                        session, config, data_stateful, self.logger
                    )
                    if response_stateful is None:
                        self.logger.debug(
                            f"{Fore.RED}A serious error occurred.{Style.RESET_ALL}"
                        )
                    response_stateful.raise_for_status()

                    # After the request completes, stop the animation
                    stop_animation.set()
                    animation_thread.join()  # Wait for the animation thread to finish
                    timeout_timer.cancel()  # Cancel the timer if the animation thread finished before the timeout
                except Exception as e:
                    self.logger.debug(
                        f"{Fore.RED}Network or server error occurred: {e}{Style.RESET_ALL}"
                    )
                    continue

                text = response_stateful.text

                json_objects = parse_jsons(text)
                combined_json = combine_json_objects(json_objects)

                content = extract_from_json(combined_json, "content")
                cleaned_list = remove_word_from_list(content, input_sentence)

                response = process_json_response(cleaned_list)

                self.interactions += 1
                try:
                    for key, value in response.items():
                        for name, text in value.items():
                            if text == "":
                                print_centered_text(
                                    f"{Fore.YELLOW}Something went wrong while processing your message. Can you click [↑] on your keyboard and press ENTER?"
                                )
                            if name in filtered_word or text is None or text == "":
                                self.logger.debug(
                                    f"{Fore.LIGHTBLACK_EX}Something went wrong. Aborting one iteration...{Style.RESET_ALL}"
                                )
                                continue
                            print(
                                f"{Fore.LIGHTBLACK_EX}[{key}]{Style.RESET_ALL} {Fore.LIGHTCYAN_EX}{name}: {Fore.LIGHTBLUE_EX}",
                                end="",
                            )
                            _message = highlight_quotes_in_text(text)
                            print_message_word_by_word(_message, 0.05)

                            if not name == "[Kiriko]" or name == f"[{userName}]":
                                message_manager.add_message(
                                    self.interactions,
                                    f"[Kiriko - {Fore.LIGHTRED_EX}Wrong format{Style.RESET_ALL}]:",
                                    text,
                                    self.logger,
                                )
                            else:
                                message_manager.add_message(
                                    self.interactions, "[Kiriko]:", text, self.logger
                                )

                            self.logger.debug(
                                f"{Fore.LIGHTBLACK_EX}<End of each>{Style.RESET_ALL}"
                            )
                        self.logger.debug(
                            f"{Fore.LIGHTBLACK_EX}<End of value>{Style.RESET_ALL}"
                        )
                    self.logger.debug(
                        f"{Fore.LIGHTBLACK_EX}<End of response>{Style.RESET_ALL}"
                    )
                except IndexError as e:
                    self.logger.error(
                        f"{Fore.YELLOW}No valid response was found.{Style.RESET_ALL} {Fore.RED}{e}{Style.RESET_ALL}"
                    )

                update_interactions(self.interactions, self.logger)
                message_manager.save_messages()
                self.logger.info(
                    f"{Fore.LIGHTCYAN_EX}Interactions value changed to: {Fore.LIGHTBLUE_EX}{self.interactions}{Style.RESET_ALL}"
                )

            except KeyboardInterrupt:
                print(f"\n{Fore.YELLOW}Program terminated by user.{Style.RESET_ALL}")
                self.logger.warning(
                    f"\n{Fore.YELLOW}Program terminated by user.{Style.RESET_ALL}"
                )
                break


if __name__ == "__main__":
    chatbot = Chatbot()
    try:
        chatbot.run()
    except Exception as e:
        print(f"{Fore.RED}Something went wrong: {e}{Style.RESET_ALL}")

    cleaner = PyCacheCleaner(".")
    cleaner.remove_pycache()
