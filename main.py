#!/usr/bin/env python3
"""
Module Docstring
"""

__author__ = "Alexander Franco"
__version__ = "0.1.1"
__license__ = "MIT"

from dotenv import load_dotenv

import src.david


def main():
    """ Main entry point of the app """
    load_dotenv()
    src.david.run()


if __name__ == "__main__":
    """ This is executed when run from the command line """
    main()
