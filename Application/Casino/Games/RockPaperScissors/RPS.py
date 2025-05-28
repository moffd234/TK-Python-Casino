import os
from random import randint
from Application.Casino.Accounts.AccountManager import AccountManager
from Application.Casino.Accounts.UserAccount import UserAccount
from Application.Casino.Games.Game import Game


def get_comp_turn() -> str:
    ran_num = randint(0, 2)
    if ran_num == 0:
        return "paper"
    elif ran_num == 1:
        return "scissors"
    else:
        return "rock"


class RPS(Game):
    def print_welcome_message(self) -> None:
        self.console.print_colored(r"""
        Yb        dP 888888 88      dP""b8  dP"Yb  8b    d8 888888     888888  dP"Yb      88""Yb 88""Yb .dP"Y8 
         Yb  db  dP  88__   88     dP   `" dP   Yb 88b  d88 88__         88   dP   Yb     88__dP 88__dP `Ybo." 
          YbdPYbdP   88""   88  .o Yb      Yb   dP 88YbdP88 88""         88   Yb   dP     88"Yb  88""''   `Y8b 
           YP  YP    888888 88ood8  YboodP  YbodP  88 YY 88 888888       88    YbodP      88  Yb 88     8bodP'
           
           Rules:
                - Normal Rock Paper Scissors rules (rock beats scissors, scissors beats paper, paper beats rock)
                - Payout is 1.25x the wager amount
        """)

    def run(self):
        self.print_welcome_message()

        while self.get_continue_input():
            wager: float = self.get_wager_amount()
            user_turn: str = self.get_user_turn()
            computer_turn: str = get_comp_turn()

            self.console.print_colored(self.handle_winner(computer_turn, user_turn, wager))

    def __init__(self, player: UserAccount, manager: AccountManager):
        super().__init__(player, manager)

    def get_user_turn(self) -> str:
        turn: str = self.console.get_string_input("Enter your turn: (Rock, Paper, Scissors)")

        while turn != "rock" and turn != "paper" and turn != "scissors":
            turn: str = self.console.get_string_input("Enter your turn: (Rock, Paper, Scissors)")

        return turn

    def handle_winner(self, comp_turn: str, user_turn: str, wager: float) -> str:
        if comp_turn == user_turn:
            return f"Draw! {user_turn.title()} ties {comp_turn}!"

        winners: dict = {
            "rock": "scissors",
            "paper": "rock",
            "scissors": "paper"
        }

        if winners[user_turn] == comp_turn:
            winnings: float = round(wager * 1.25, 2)

            self.manager.add_and_save_account(self.player, winnings)
            return f"You won! {user_turn.title()} beats {comp_turn}!"

        # ASSERT: CPU has winning move
        return f"You lost! {user_turn.title()} loses to {comp_turn}!"


def main():
    account_manager: AccountManager = AccountManager()
    account: UserAccount = UserAccount("Tester", "ValidPassword123!", 1000, "test@email.com",
                                       ["Who is your favorite sports team?", "Test Answer",
                                        "What street did you grow up on?", "Test Street"])
    game: RPS = RPS(account, account_manager)
    game.run()

    if os.path.exists("casino.db"):
        os.remove("casino.db")


if __name__ == "__main__":
    main()
