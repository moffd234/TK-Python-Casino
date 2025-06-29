from Application.Controller.AccountController import AccountController
from Application.Model.Games.CoinFlip.CoinFlip import handle_heads_tails
from Application.Model.Games.GameOutcome import GameOutcome


class CoinFlipController:

    def __init__(self, account_controller: AccountController):
        self.account_controller = account_controller

    def handle_outcome(self, guess: str, wager: float) -> GameOutcome:
        """
        Handles the logic of a coin flip game, including checking the user's guess,
        updating account balance based on the result, and returning the outcome.

        :param guess: The user's guess for the coin flip ("heads" or "tails").
        :param wager: The amount of money the user is wagering.
        :return: GameOutcome indicating WIN, LOSS, or WITHDRAW_ERROR.
        """
        flip: str = handle_heads_tails()
        successful_withdraw: bool = self.account_controller.subtract_losses(wager)

        if successful_withdraw:
            if flip == guess:
                self.account_controller.add_winnings(wager * 1.25)
                return GameOutcome.WIN

            return GameOutcome.LOSS

        return GameOutcome.WITHDRAW_ERROR
