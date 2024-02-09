import requests
from colorama import Fore, Style


def setup_session(config, logger):
    """Setup and return a session with custom headers and cookies."""
    try:
        session = requests.Session()
        session.headers.update(
            {
                "User-Agent": config["SESSION"]["User-Agent"],
                "Accept": "*/*",
                "Accept-Encoding": "gzip, deflate, br",
                "Accept-Language": config["SESSION"]["Accept-Language"],
                "Origin": config["SESSION"]["Origin"],
                "Referer": config["SESSION"]["Referer"],
                "Content-Type": "application/json",
            }
        )

        session.cookies.set(
            "auth_organization",
            config["COOKIES"]["auth_organization"],
            domain="dreamgen.com",
        )
        session.cookies.set(
            "auth_session", config["COOKIES"]["auth_session"], domain="dreamgen.com"
        )

        logger.info(f"{Fore.GREEN}Session setup successfully.{Style.RESET_ALL}")
        return session
    except Exception as e:
        logger.error(f"{Fore.RED}Error setting up session: {e}{Style.RESET_ALL}")
        return None


def post_event(session, config, data_event, logger):
    """Post an event with the given session and return the response."""
    try:
        response = session.post(config["API"]["url_event"], json=data_event)
        return response
    except Exception as e:
        logger.error(f"{Fore.RED}Error posting event: {e}{Style.RESET_ALL}")
        return None


def post_stateful(session, config, data_stateful, logger):
    """Post stateful data with the given session and return the response."""
    try:
        response = session.post(config["API"]["url_stateful"], json=data_stateful)
        return response
    except Exception as e:
        print(f"{Fore.RED}Error posting stateful data: {e}{Style.RESET_ALL}")
        return None
