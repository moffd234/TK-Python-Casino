import os.path
import random

from Application.Casino.Accounts.AccountManager import AccountManager
from Application.Casino.Accounts.UserAccount import UserAccount
from Application.Casino.Games.Game import Game
from Application.Utils.ANSI_COLORS import ANSI_COLORS


def handle_heads_tails() -> str:
    flip_num: int = random.randint(0, 1)
    return "tails" if flip_num == 0 else "heads"


class CoinFlip(Game):

    def __init__(self, player: UserAccount, manager: AccountManager):
        super().__init__(player, manager)
        self.console.color = ANSI_COLORS.BLUE.value

    def print_welcome_message(self) -> None:
        self.console.print_colored(r"""
        
        Yb        dP 888888 88      dP""b8  dP"Yb  8b    d8 888888     888888  dP"Yb       dP""b8  dP"Yb  88 88b 88     888888 88     88 88""Yb 
         Yb  db  dP  88__   88     dP   `" dP   Yb 88b  d88 88__         88   dP   Yb     dP   `" dP   Yb 88 88Yb88     88__   88     88 88__dP 
          YbdPYbdP   88""   88  .o Yb      Yb   dP 88YbdP88 88""         88   Yb   dP     Yb      Yb   dP 88 88 Y88     88""   88  .o 88 88
           YP  YP    888888 88ood8  YboodP  YbodP  88 YY 88 888888       88    YbodP       YboodP  YbodP  88 88  Y8     88     88ood8 88 88     
        
        rules:
             1. Enter a guess of either heads or tails
             2. A coin will be flipped
             3. If you guess correctly you will win 1.25x your wager
        """)

    def run(self):
        self.print_welcome_message()

        while self.get_continue_input():
            wager: float = self.get_wager_amount()

            flip: str = handle_heads_tails()
            guess: str = self.get_guess()

            self.console.print_colored(self.handle_outcome(guess, flip, wager))

    def get_guess(self) -> str:
        guess: str = self.console.get_string_input("Enter your guess: (heads or tails)")

        while guess != "heads" and guess != "tails":
            self.console.print_error("Guess must be 'heads' or 'tails'")
            guess = self.console.get_string_input("Enter your guess: (heads or tails)")

        return guess

    def handle_outcome(self, guess: str, flip: str, wager: float):
        if guess == flip:
            self.manager.add_and_save_account(self.player, wager * 1.25)
            return f"You Won! The coin was {flip}"

        else:
            return f"You Loss! The coin was {flip}"


def main():
    import os

    account_manager: AccountManager = AccountManager()
    account: UserAccount = UserAccount("Tester", "ValidPassword123!", 1000, "test@email.com",
                                       ["Who is your favorite sports team?", "Test Answer",
                                        "What street did you grow up on?", "Test Street"])
    game: CoinFlip = CoinFlip(account, account_manager)
    game.run()

    if os.path.exists("casino.db"):
        os.remove("casino.db")


if __name__ == "__main__":
    main()
