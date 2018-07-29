#coding: utf-8

__author__  = "@DFIRENCE | CARLOS DIAZ"
__version__ = "0.0.1"
__license__ = "MIT"

from colorama import init
from colorama import Fore
from colorama import Back
from colorama import Style

from platform import platform

init(autoreset=True)

class Palette(object):
    def __init__(self):
        self.color = self.bright_foreground()

    def bright_foreground(self):
        color = {
            'red'       : '{0}{1}'.format(Fore.RED, Style.BRIGHT),
            'cyan'      : '{0}{1}'.format(Fore.CYAN, Style.BRIGHT),
            'green'     : '{0}{1}'.format(Fore.GREEN, Style.BRIGHT),
            'yellow'    : '{0}{1}'.format(Fore.YELLOW, Style.BRIGHT),
            'blue'      : '{0}{1}'.format(Fore.BLUE, Style.BRIGHT),
            'magenta'   : '{0}{1}'.format(Fore.MAGENTA, Style.BRIGHT),
            'white'     : '{0}{1}'.format(Fore.WHITE, Style.BRIGHT),
            'grey'      : '{0}{1}'.format(Fore.WHITE, Style.RESET_ALL)
        }
        return color
