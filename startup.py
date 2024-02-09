import argparse
import subprocess
from colorama import Fore, Style, init, deinit

# Initialize colorama to auto-reset style after each print
init(autoreset=True)

class ToolLauncher:
    def __init__(self):
        self.parser = self.setup_parser()

    def setup_parser(self):
        parser = argparse.ArgumentParser(description="Tool Launcher", add_help=False)
        # Updated to include short options for each tool
        parser.add_argument('-t', '--tags', type=str, required=False, help='The tool to launch')
        parser.add_argument('-h', '--help', action='store_true', help='Show this help message and exit')
        return parser

    def run(self):
        args = self.parser.parse_args()
        if args.help or not args.tags:
            self.print_help()
        elif args.tags in ['config_editor', 'ce']:
            self.launch_config_editor()
        elif args.tags in ['data_extractor', 'dataex']:
            self.launch_data_extractor()
        elif args.tags in ['start', 'main']:
            self.launch_main()

    def launch_config_editor(self):
        print(f"{Fore.CYAN}Launching{Style.RESET_ALL} {Fore.LIGHTCYAN_EX}'Config Editor'{Fore.CYAN}...{Style.RESET_ALL}")
        deinit()
        subprocess.run("python GUI_config_editor.py", shell=True)

    def launch_data_extractor(self):
        print(f"{Fore.CYAN}Launching{Style.RESET_ALL} {Fore.LIGHTCYAN_EX}'Data Extractor'{Fore.CYAN}...{Style.RESET_ALL}")
        deinit()
        subprocess.run("python GUI_data_extractor.py", shell=True)

    def launch_main(self):
        print(f"{Fore.CYAN}Launching{Style.RESET_ALL} {Fore.LIGHTCYAN_EX}'Main Script'{Fore.CYAN}...{Style.RESET_ALL}")
        deinit()
        subprocess.run("python main.py", shell=True)

    def print_help(self):
        help_text = f"""
{Fore.CYAN}Tool Launcher Help{Style.RESET_ALL}

Usage: 
    startup.py [-t TOOL_NAME] [options]

Tools:
    -t, --tags TOOL_NAME            Launch a specific tool. Options are 'ce' or 'config_editor', 'dataex' or 'data_extractor', 'start' or 'main'.
                                    If no tool is specified, the help message is shown.

Options:
    -h, --help                      Show this help message and exit.

{Fore.YELLOW}Examples:{Style.RESET_ALL}
    {Fore.LIGHTCYAN_EX}startup.py{Style.RESET_ALL} {Fore.LIGHTMAGENTA_EX}--tags{Style.RESET_ALL} {Fore.LIGHTBLUE_EX}config_editor{Style.RESET_ALL}
    {Fore.LIGHTCYAN_EX}startup.py{Style.RESET_ALL} {Fore.LIGHTMAGENTA_EX}--tags{Style.RESET_ALL} {Fore.LIGHTBLUE_EX}data_extractor{Style.RESET_ALL}
    {Fore.LIGHTCYAN_EX}startup.py{Style.RESET_ALL} {Fore.LIGHTMAGENTA_EX}--tags{Style.RESET_ALL} {Fore.LIGHTBLUE_EX}start{Style.RESET_ALL}
    {Fore.LIGHTCYAN_EX}startup.py{Style.RESET_ALL} {Fore.LIGHTMAGENTA_EX}-t{Style.RESET_ALL}     {Fore.LIGHTBLUE_EX}ce{Style.RESET_ALL}
    {Fore.LIGHTCYAN_EX}startup.py{Style.RESET_ALL} {Fore.LIGHTMAGENTA_EX}-t{Style.RESET_ALL}     {Fore.LIGHTBLUE_EX}dataex{Style.RESET_ALL}
    {Fore.LIGHTCYAN_EX}startup.py{Style.RESET_ALL} {Fore.LIGHTMAGENTA_EX}-t{Style.RESET_ALL}     {Fore.LIGHTBLUE_EX}main{Style.RESET_ALL}

{Fore.RED}Note:{Style.RESET_ALL}
    This script serves as a launcher for different tools, including the main script.
    Each tool has its own set of options and functionalities.
    For help with a specific tool, launch the tool with the '{Fore.LIGHTMAGENTA_EX}--help{Style.RESET_ALL}' option to see more details."""
        print(help_text)
        deinit()

if __name__ == "__main__":
    launcher = ToolLauncher()
    launcher.run()
    print(f"{Fore.LIGHTCYAN_EX}Exiting...{Style.RESET_ALL}")
    deinit()
