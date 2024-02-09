from colorama import Fore, Style
import json


def get_valid_interactions(backup_file, default_interactions):
    """
    Fetches the number of interactions from a backup file.

    Parameters:
    - backup_file: Path to the backup JSON file.
    - default_interactions: Default interaction count to return if the file doesn't exist or an error occurs.

    Returns:
    - The number of interactions found in the backup file or the default value.
    """
    try:
        with open(backup_file, "r") as file:
            data = json.load(file)
            interactions = data.get("interactions", default_interactions)
            return interactions
    except FileNotFoundError:
        print(
            f"{Fore.RED}Backup file '{backup_file}' not found. Using default interactions.{Style.RESET_ALL}"
        )
    except json.JSONDecodeError:
        print(
            f"{Fore.RED}Error decoding JSON from file '{backup_file}'. Using default interactions.{Style.RESET_ALL}"
        )
    except Exception as e:
        print(
            f"{Fore.RED}An unexpected error occurred: {e}. Using default interactions.{Style.RESET_ALL}"
        )

    return default_interactions


def get_user_confirmation(backup_file, default_interactions, logger):
    interactions = get_valid_interactions(backup_file, default_interactions)
    print(
        f"{Fore.GREEN}Interactions set to:{Style.RESET_ALL} {Fore.LIGHTYELLOW_EX}{interactions}{Style.RESET_ALL}"
    )
    logger.info(
        f"{Fore.GREEN}Interactions set to:{Style.RESET_ALL} {Fore.LIGHTYELLOW_EX}{interactions}{Style.RESET_ALL}"
    )

    while True:
        user_input = (
            input("Is this number of interactions correct? (Y/N): ").strip().lower()
        )
        if user_input in ["y", "yes"]:
            return interactions
        elif user_input in ["n", "no"]:
            try:
                interactions = int(
                    input("Please enter the new number of interactions: ")
                )
                print(
                    f"{Fore.GREEN}New number of interactions set to:{Style.RESET_ALL} {Fore.LIGHTYELLOW_EX}{interactions}{Style.RESET_ALL}"
                )
                logger.info(
                    f"{Fore.GREEN}New number of interactions set to:{Style.RESET_ALL} {Fore.LIGHTYELLOW_EX}{interactions}{Style.RESET_ALL}"
                )
                return interactions
            except ValueError as e:
                print(
                    f"{Fore.RED}Invalid input. Please enter a valid number.\n{e}{Style.RESET_ALL}"
                )
                logger.info(f"{Fore.RED}Invalid input: {e}{Style.RESET_ALL}")
        else:
            print(
                f"{Fore.RED}Invalid response. Please answer 'Y' for Yes or 'N' for No.{Style.RESET_ALL}"
            )
            logger.info(f"{Fore.RED}Invalid response: {user_input}{Style.RESET_ALL}")
