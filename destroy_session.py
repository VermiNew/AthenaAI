import os
import shutil
from tqdm import tqdm
from zipfile import ZipFile
import datetime
from colorama import init, Fore, Style

# Initialize Colorama
init(autoreset=True)


def destroy_session():
    steps = [
        "Entering the 'data' folder",
        "Creating ZIP archive of 'config.ini'",
        "Moving ZIP archive to 'data/.archive'",
        "Overwriting 'backup.json'",
        "Deleting 'config.ini'",
        "Copying 'default_config.ini' as 'config.ini'",
        "Exiting the 'data' folder",
        "Deleting 'chatbot.log'",
        "Entering the 'conv' folder",
        "Deleting 'messages_history.json'",
        "Exiting the 'conv' folder",
    ]

    with tqdm(total=len(steps), desc="Destroying session") as pbar:
        for step in steps:
            if step == "Entering the 'data' folder":
                os.chdir("data")
            elif step == "Creating ZIP archive of 'config.ini'":
                archive_name = f"config_backup_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.zip"
                with ZipFile(archive_name, "w") as zipf:
                    zipf.write("config.ini")
            elif step == "Moving ZIP archive to 'data/.archive'":
                archive_folder = ".archive"
                if not os.path.exists(archive_folder):
                    os.makedirs(archive_folder)
                shutil.move(archive_name, os.path.join(archive_folder, archive_name))
            elif step == "Overwriting 'backup.json'":
                with open("backup.json", "w") as f:
                    f.write("{}")
            elif step == "Deleting 'config.ini'":
                os.remove("config.ini")
            elif step == "Copying 'default_config.ini' as 'config.ini'":
                shutil.copy("default_config.ini", "config.ini")
            elif step == "Exiting the 'data' folder":
                os.chdir("..")
            elif step == "Deleting 'chatbot.log'":
                if os.path.exists("chatbot.log"):
                    os.remove("chatbot.log")
            elif step == "Entering the 'conv' folder":
                os.chdir("conv")
            elif step == "Deleting 'messages_history.json'":
                if os.path.exists("messages_history.json"):
                    os.remove("messages_history.json")
            elif step == "Exiting the 'conv' folder":
                os.chdir("..")

            # Update tqdm progress bar description with colored text
            pbar.set_description_str(f"{Fore.CYAN}{step}{Style.RESET_ALL}")
            pbar.update(1)


if __name__ == "__main__":
    destroy_session()
    print(f"{Fore.GREEN}Session destroyed successfully.{Style.RESET_ALL}")
