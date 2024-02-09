import time
import re


def print_message_word_by_word(message, delay=0):
    """
    Prints a message word by word with a specified delay between each word.

    :param message: The message to be printed word by word.
    :param delay: The delay (in seconds) between each word. It's disabled by default.
    """

    # Split the message into words
    words = message.split()

    # Print each word with the specified delay
    for word in words:
        print(word, end=" ", flush=True)
        time.sleep(delay)

    # Print a newline character at the end of the message
    print()


def process_json_response(data):
    messages = {}
    current_speaker = None

    for item in data:
        if item.endswith(":"):
            current_speaker = item.replace(":", "")
            messages[current_speaker] = ""
        else:
            cleaned_item = item
            if (
                current_speaker
                and cleaned_item
                and (
                    not messages[current_speaker]
                    or cleaned_item.startswith(messages[current_speaker])
                )
            ):
                messages[current_speaker] = cleaned_item

    # Tworzenie nowego słownika do zwrócenia
    ordered_messages = {}
    for index, (speaker, message) in enumerate(messages.items()):
        ordered_messages[index] = {speaker: message}

    return ordered_messages


def is_input_well_formed(input_sentence, logger):
    """
    Checks if the input sentence is well-formed according to the specified rules,
    and logs a warning if not.

    Parameters:
    - input_sentence (str): The sentence to be checked.
    - logger (logging.Logger): An instance of a logger to log warnings.

    Returns:
    - bool: True if the sentence is well-formed according to the specified rules, False otherwise.
    """
    # Trim outer whitespace
    trimmed_input = input_sentence.strip()

    # Define the pattern based on whether the sentence is expected to start with a quotation mark
    if trimmed_input.startswith('"'):
        pattern = r'^"\s*\S.*\S\s*"$'
    else:
        pattern = (
            r"^\S.*\S$|^.$"  # Match non-whitespace start and end or single character
        )

    # Check if the input matches the pattern
    well_formed = bool(re.match(pattern, trimmed_input))

    # Log a warning if the input is not well-formed
    if not well_formed:
        logger.warning(f"Malformed input detected: {input_sentence}")

    return well_formed
