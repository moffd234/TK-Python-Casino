import random

from Application.Model.Accounts.AccountManager import AccountManager
from Application.Model.Accounts.UserAccount import UserAccount
from Application.Model.Games.Game import Game
from Application.Utils.ANSI_COLORS import ANSI_COLORS


def handle_heads_tails() -> str:
    flip_num: int = random.randint(0, 1)
    return "tails" if flip_num == 0 else "heads"


class CoinFlip(Game):

    def __init__(self):
        super().__init__()
        self.console.color = ANSI_COLORS.BLUE.value

    def get_guess(self) -> str:
        guess: str = self.console.get_string_input("Enter your guess: (heads or tails)")

        while guess != "heads" and guess != "tails":
            self.console.print_error("Guess must be 'heads' or 'tails'")
            guess = self.console.get_string_input("Enter your guess: (heads or tails)")

        return guess

    def handle_outcome(self, guess: str, flip: str, wager: float):
        if guess == flip:
            return f"You Won! The coin was {flip}"

        else:
            return f"You Loss! The coin was {flip}"
