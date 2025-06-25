from Application.Controller.AccountController import AccountController
from Application.Controller.Games.CoinFlipController import CoinFlipController


class GameController:
    def __init__(self, account_controller: AccountController):
        self.account_controller: AccountController = account_controller
        self.cf_controller = CoinFlipController(account_controller)
