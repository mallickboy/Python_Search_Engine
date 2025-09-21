from datetime import datetime
from enum import Enum
from colorama import Fore, Style, init

# Initializing colorama globally (once for all imports) for cross-platform support
init(autoreset=True)   

class Color(Enum):
    """
    Enum for terminal text colors.

    Uses colorama's Fore constants to enable type-safe usage
    of color values across the application.
    """
    CYAN = Fore.CYAN
    GREEN = Fore.GREEN
    RED = Fore.RED
    YELLOW = Fore.YELLOW

def log(msg: str, verbose: bool = False, color: Color = Color.CYAN) -> None:
    """
    Print a timestamped log message if verbose is enabled.
    """
    if verbose:
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(f"\n{color.value}[{timestamp}] [log]{Style.RESET_ALL} {msg}", end="")