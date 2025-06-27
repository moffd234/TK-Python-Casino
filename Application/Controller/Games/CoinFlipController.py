from Application.Controller.AccountController import AccountController
from Application.Model.Games.CoinFlip.CoinFlip import handle_heads_tails


class CoinFlipController:

    def __init__(self, account_controller: AccountController):
        self.account_controller = account_controller

    def handle_outcome(self, guess: str, wager: float) -> bool:
        flip: str = handle_heads_tails()
        if flip == guess:
            self.account_controller.add_winnings(wager * 1.25)
            return True

        self.account_controller.subtract_losses(wager)
        return False
