import atexit
import signal
import threading
import time
from json_memory_manager import (
    storeMemoryJson,
)
from colorama import Fore, Style

# Global variable to store interactions
global_interactions = 0


def update_interactions(new_count, logger):
    """Updates the global interactions count."""
    global global_interactions
    logger.debug(f"{Fore.LIGHTBLUE_EX}Old value: {Fore.CYAN}{global_interactions}{Style.RESET_ALL}")
    global_interactions = new_count
    logger.debug(f"{Fore.LIGHTBLUE_EX}New value: {Fore.CYAN}{global_interactions}{Style.RESET_ALL}")


def save_interactions(backup_path, logger):
    """Saves the current value of 'global_interactions' to a JSON file."""
    try:
        storeMemoryJson(backup_path, "interactions", global_interactions, logger)
        logger.info(f"{Fore.GREEN}Interactions saved successfully.{Style.RESET_ALL}")
    except Exception as e:
        logger.error(f"{Fore.RED}Failed to save interactions: {e}{Style.RESET_ALL}")


def exit_handler(backup_path, logger):
    """Function called upon program exit to save state."""
    logger.info(f"{Fore.YELLOW}Saving state before exiting...{Style.RESET_ALL}")
    save_interactions(backup_path, logger)


def signal_handler(signum, frame, backup_path, logger):
    """Handles signals like SIGINT (Ctrl+C) and SIGTERM, ensuring data is saved before exit."""
    exit_handler(backup_path, logger)
    logger.info(f"{Fore.YELLOW}Closing...{Style.RESET_ALL}")
    exit(1)


def periodic_save(interval, backup_path, logger):
    """Periodically saves the 'global_interactions' value at a specified interval."""
    while True:
        time.sleep(interval)
        logger.info(f"{Fore.CYAN}Automatic saving...{Style.RESET_ALL}")
        save_interactions(backup_path, logger)


def start_background_saving(interval, backup_path, logger):
    """Starts a background thread that periodically saves data."""
    background_saver = threading.Thread(
        target=lambda: periodic_save(interval, backup_path, logger), daemon=True
    )
    background_saver.start()
    logger.info(
        f"{Fore.GREEN}Backup saver function started!{Style.RESET_ALL} {Fore.LIGHTBLUE_EX}Interval:{Style.RESET_ALL} {Fore.LIGHTCYAN_EX}{interval}{Style.RESET_ALL}"
    )


def register_signal_handlers(backup_path, logger):
    """Registers signal handlers that include necessary parameters for graceful shutdown."""
    signal.signal(
        signal.SIGINT, lambda signum, frame: signal_handler(signum, frame, backup_path, logger)
    )
    signal.signal(
        signal.SIGTERM, lambda signum, frame: signal_handler(signum, frame, backup_path, logger)
    )
    logger.info(f"{Fore.GREEN}Signal handlers registered!{Style.RESET_ALL}")


def register_exit_handler(backup_path, logger):
    """Registers an exit handler function that is called when the program exits."""
    atexit.register(lambda: exit_handler(backup_path, logger))
    logger.info(f"{Fore.GREEN}Exit handler registered!{Style.RESET_ALL}")
