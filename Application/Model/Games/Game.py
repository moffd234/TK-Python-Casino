from abc import ABC, abstractmethod

from Application.Utils.IOConsole import IOConsole


class Game(ABC):
    def __init__(self):
        self.console = IOConsole()
