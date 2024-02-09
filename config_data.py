from colorama import Fore, Style


def generate_data(config, user_input, interactions):
    try:
        # Prepare data_event
        data_event = {
            "n": "RpSessionContinue",
            "u": config["SESSION"]["Referer"],
            "d": "dreamgen.com",
            "r": "https://dreamgen.com/app/rp/scenarios/sessions",
            "p": {
                "modelId": config["MODEL"]["modelId"],
                "newInteractionCount": 1,
                "interactionsCount": interactions,
            },
        }

        # Prepare data_stateful
        data_stateful = {
            "sessionId": config["IDENTIFICATION"]["sessionId"],
            "modelId": config["MODEL"]["modelId"],
            "promptParams": {
                "keepOnlyLastInstruction": False,
                "pruneInteractionsAboveTokenLimit": True,
            },
            "samplingParams": {
                "kind": config["SamplingParams"]["kind"],
                "maxTokens": int(config["SamplingParams"]["maxTokens"]),
                "temperature": float(config["SamplingParams"]["temperature"]),
                "topP": float(config["SamplingParams"]["topP"]),
                "topK": int(config["SamplingParams"]["topK"]),
                "minP": float(config["SamplingParams"]["minP"]),
                "frequencyPenalty": float(config["SamplingParams"]["frequencyPenalty"]),
                "presencePenalty": float(config["SamplingParams"]["presencePenalty"]),
                "repetitionPenalty": float(
                    config["SamplingParams"]["repetitionPenalty"]
                ),
                "ignoreEos": config["SamplingParams"]["ignoreEos"] == "True",
                "stopConditions": {
                    "stopAfterInteractions": int(
                        config["SamplingParams"]["stopAfterInteractions"]
                    ),
                    "stopBeforeUserMessage": config["SamplingParams"][
                        "stopBeforeUserMessage"
                    ]
                    == "True",
                },
                "allowedRoles": [config["SamplingParams"]["allowedRoles"]],
            },
            "editorParams": {"showHiddenInteractions": False},
            "newInteractions": [
                {
                    "payload": {
                        "type": "message",
                        "role": "user",
                        "name": "",
                        "content": user_input,
                        "closed": True,
                        "hidden": False,
                        "excluded": False,
                        "sticky": False,
                    }
                }
            ],
        }

        # Everything went well
        return data_event, data_stateful, 0

    except Exception as e:
        print(f"{Fore.RED}Error generating data: {e}{Style.RESET_ALL}")
        # Return None for data_event and data_stateful in case of error, with a non-zero status code
        return None, None, -1


def load_credentials(config):
    """
    Loads the 'name' value from the 'Credentials' section of a loaded config object.

    Parameters:
    config (configparser.ConfigParser): Loaded configuration object.

    Returns:
    dict: A dictionary with the 'name' key and its value.
    """
    credentials = {}

    if "Credentials" in config:
        if "name" in config["Credentials"]:
            credentials["name"] = config["Credentials"]["name"]

    return credentials


def format_filtered_word(credentials):
    """
    Formats the 'name' value from credentials into a string enclosed in square brackets.

    Parameters:
    credentials (dict): A dictionary with the 'name' key and its value.

    Returns:
    str: The formatted string.
    """
    name = credentials.get("name", "")
    return f"[{name}]"


def print_credentials(config):
    """
    Prints the credentials from the config.

    Parameters:
    config (ConfigParser): The ConfigParser object containing the configuration.
    """
    if config.has_section("Credentials"):
        print(f"{Fore.LIGHTYELLOW_EX}Credentials:{Style.RESET_ALL}")
        for key in config["Credentials"]:
            print(
                f"{Fore.LIGHTWHITE_EX}{key}: {config['Credentials'][key]}{Style.RESET_ALL}"
            )
