import os
import random

from Application.Casino.Accounts.AccountManager import AccountManager
from Application.Casino.Accounts.UserAccount import UserAccount
from Application.Casino.Games.Game import Game
from Application.Utils.ANSI_COLORS import ANSI_COLORS


def get_spin() -> list[str]:
    possibilities: list[str] = ["7️⃣", "🔔", "🔔", "⬛", "⬛", "⬛", "🍒", "🍒", "🍒", "🍒", "🍒"]
    random.shuffle(possibilities)
    return possibilities[:3]

def handle_spin(spin: list[str]) -> float:
    if spin[0] != spin[1] or spin[0] != spin[2]:
        return 0

    payouts = {"7️⃣": 10, "🔔": 5, "⬛": 2, "🍒": 1.5}

    return payouts[spin[0]]


def get_payout(wager: float, spin: list[str]) -> float:
    multiplier: float = handle_spin(spin)
    return round(multiplier * wager, 2)



class Slots(Game):

    def __init__(self, player: UserAccount, manager: AccountManager):
        super().__init__(player, manager)

    def print_welcome_message(self) -> None:
        self.console.print_colored(r"""        
        Yb        dP 888888 88      dP""b8  dP"Yb  8b    d8 888888     888888  dP"Yb      .dP"Y8 88      dP"Yb  888888 .dP"Y8 
         Yb  db  dP  88__   88     dP   `" dP   Yb 88b  d88 88__         88   dP   Yb     `Ybo." 88     dP   Yb   88   `Ybo." 
          YbdPYbdP   88""   88  .o Yb      Yb   dP 88YbdP88 88""         88   Yb   dP     o.`Y8b 88  .o Yb   dP   88   o.`Y8b 
           YP  YP    888888 88ood8  YboodP  YbodP  88 YY 88 888888       88    YbodP      8bodP' 88ood8  YbodP    88   8bodP' 
           
           Rules:
                - 1. Enter a wager amount.
                - 2. Match three symbols on the pay line to win
                - 3. Payouts vary based on the symbols matched:
                     - Three 7s: Jackpot(10x)
                     - Three Bells: Big Win(5x)
                     - Three Bars: Medium Win (2x)
                     - Three Cherries: Small Win (1.5x)
                     - Any other combination: No Win (You lose your wager)
        """)

    def run(self):
        self.print_welcome_message()

        while self.get_continue_input():
            wager: float = self.get_wager_amount()
            spin: list[str] = get_spin()
            self.print_spin(spin)
            payout: float = get_payout(wager, spin)

            if payout != 0:
                self.console.print_colored(f"Congrats you won! ${payout} has been added to your account!",
                                                 ANSI_COLORS.GREEN)
                self.manager.add_and_save_account(self.player, payout)

            else:
                self.console.print_colored("Sorry, you lost")

    def print_spin(self, spin: list[str]) -> None:
        self.console.print_colored("\n🎰 Spinning... 🎰\n")
        self.console.print_colored("┌───┬───┬───┐")
        self.console.print_colored(f"│ {spin[0]}│ {spin[1]}│ {spin[2]}│")
        self.console.print_colored("└───┴───┴───┘\n")


def main():

    account_manager: AccountManager = AccountManager()
    account: UserAccount = UserAccount("Tester", "ValidPassword123!", 1000, "test_username",
                                       ["Who is your favorite sports team?", "Test Answer",
                                        "What street did you grow up on?", "Test Street"])
    game: Slots = Slots(account, account_manager)
    game.run()

    if os.path.exists("casino.db"):
        os.remove("casino.db")


if __name__ == "__main__":
    main()