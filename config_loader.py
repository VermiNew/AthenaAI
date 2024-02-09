from configparser import ConfigParser
from colorama import Fore, Style


def load_config(config_file, logger):
    try:
        config = ConfigParser()
        config.read(config_file)
    except Exception as e:
        logger.error(f"An error occured: {e}")
        return None
    logger.info(
        f"{Fore.GREEN}Config successfully loaded!{Fore.LIGHTBLUE_EX} File:{Style.RESET_ALL} {Fore.LIGHTCYAN_EX}'{config_file}'{Style.RESET_ALL}"
    )
    return config


def get_config_info(config, logger, section=None, parameter=None):
    """
    Fetches and prints information from a given section or parameter within a
    configparser instance. Can return information from an entire section or a
    specific parameter within that section.

    Parameters:
    - config: An instance of configparser.ConfigParser().
    - logger: An instance of a logger.
    - section: Optional. The name of the section to fetch information from. If None,
               information from all sections will be printed and returned.
    - parameter: Optional. The specific parameter to fetch from the section. This
                 requires 'section' to be specified.

    Returns:
    - A dictionary with information from the specified section(s), or
    - A specific parameter's value if 'parameter' is specified, or
    - None if the specified section/parameter does not exist.
    """
    try:
        if section:
            if section not in config.sections():
                logger.error(
                    f"{Fore.RED}Error: The [{section}] section does not exist in the config.{Style.RESET_ALL}"
                )
                return None
            if parameter:
                if parameter in config[section]:
                    value = config[section][parameter]
                    logger.info(
                        f"{Fore.GREEN}Parameter value from [{section}]: {Fore.LIGHTCYAN_EX}{parameter} = {Fore.CYAN}{value}{Style.RESET_ALL}"
                    )
                    return value
                else:
                    logger.error(
                        f"{Fore.RED}Error: The parameter '{parameter}' does not exist in the [{section}] section.{Style.RESET_ALL}"
                    )
                    return None
            else:
                section_info = dict(config.items(section))
                logger.info(f"{Fore.GREEN}Information from [{section}]:")
                for key, value in section_info.items():
                    logger.info(f"{Fore.YELLOW}{key}: {Fore.CYAN}{value}{Style.RESET_ALL}")
                return section_info
        else:
            all_info = {
                section: dict(config.items(section)) for section in config.sections()
            }
            for section, parameters in all_info.items():
                logger.info(f"{Fore.GREEN}Information from [{section}]:")
                for key, value in parameters.items():
                    logger.info(f"{Fore.YELLOW}{key}: {Fore.CYAN}{value}{Style.RESET_ALL}")
            return all_info

    except Exception as e:
        logger.error(f"{Fore.RED}An error occurred: {e}{Style.RESET_ALL}")
        return None
