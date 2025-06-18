from abc import ABC, abstractmethod

from Application.Utils.IOConsole import IOConsole


class Game(ABC):
    def __init__(self):
        self.console = IOConsole()

    @abstractmethod
    def print_welcome_message(self) -> None:
        pass

    @abstractmethod
    def run(self):
        pass

    def get_continue_input(self) -> bool:
        return self.console.get_boolean_input("Would you like to keep playing?")
