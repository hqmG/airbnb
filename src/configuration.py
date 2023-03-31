"""
Configuration script.
"""
# Modules
from dotenv import find_dotenv
import os
from pathlib import Path


def change_root() -> None:
    """
    Changing root directory.
    """
    # Directory
    os.chdir(Path(find_dotenv()).parent)


if __name__ == '__main__':

    # Changing root
    change_root()
