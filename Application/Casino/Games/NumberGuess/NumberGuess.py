import os
import random

from Application.Casino.Accounts.AccountManager import AccountManager
from Application.Casino.Accounts.UserAccount import UserAccount
from Application.Utils.ANSI_COLORS import ANSI_COLORS
from Application.Casino.Games.Game import Game


class NumberGuess(Game):
    def __init__(self, player: UserAccount, manager: AccountManager):
        super().__init__(player, manager)
        self.console.color = ANSI_COLORS.CYAN.value

    def print_welcome_message(self) -> None:
        self.console.print_colored(r"""
        
        Yb        dP 888888 88      dP""b8  dP"Yb  8b    d8 888888     888888  dP"Yb      88b 88 88   88 8b    d8      dP""b8 88   88 888888 .dP"Y8 .dP"Y8 
         Yb  db  dP  88__   88     dP   `" dP   Yb 88b  d88 88__         88   dP   Yb     88Yb88 88   88 88b  d88     dP   `" 88   88 88__   `Ybo." `Ybo." 
          YbdPYbdP   88""   88  .o Yb      Yb   dP 88YbdP88 88""         88   Yb   dP     88 Y88 Y8   8P 88YbdP88     Yb  "88 Y8   8P 88""   o.`Y8b o.`Y8b 
           YP  YP    888888 88ood8  YboodP  YbodP  88 YY 88 888888       88    YbodP      88  Y8 `YbodP' 88 YY 88      YboodP `YbodP' 888888 8bodP' 8bodP' 
           
           Rules:
                1. A random integer will be generated from 1 to 10 (including 1 and 10)
                2. You will get one chance to input a guess
                3. If you are right you will win 2x your wager
        """)

    def run(self):
        self.print_welcome_message()

        while self.get_continue_input():
            num: int = random.randint(1, 10)  # From 1 to 10 [inclusive]
            wager: float = self.get_wager_amount()
            guess: int = self.get_guess()
            self.console.print_colored(self.handle_guess(guess, num, wager))

    def get_guess(self) -> int:
        guess: int = self.console.get_integer_input("Enter your guess from 1 - 10 (inclusive)")

        while guess < 1 or guess > 10:
            self.console.print_error("Number should be from 1 - 10 (inclusive)")
            guess = self.console.get_integer_input("Enter your guess from 1 - 10")

        return guess

    def handle_guess(self, guess: int, ran_num: int, wager: float) -> str:
        if guess == ran_num:
            self.manager.add_and_save_account(self.player, wager * 2)
            return f"You Won! The answer was {ran_num}"

        return f"You lost. The answer was {ran_num}"


def main():
    account_manager: AccountManager = AccountManager()
    account: UserAccount = UserAccount("Tester", "ValidPassword123!", 1000, "test@email.com",
                                       ["Who is your favorite sports team?", "Test Answer",
                                        "What street did you grow up on?", "Test Street"])
    game: NumberGuess = NumberGuess(account, account_manager)
    game.run()

    if os.path.exists("casino.db"):
        os.remove("casino.db")


if __name__ == "__main__":
    main()
