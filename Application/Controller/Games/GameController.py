from Application.Controller.AccountController import AccountController
from Application.Controller.Games.CoinFlipController import CoinFlipController
from Application.Controller.Games.TriviaController import TriviaController


class GameController:
    def __init__(self, account_controller: AccountController):
        self.account_controller: AccountController = account_controller
        self.cf_controller: CoinFlipController = CoinFlipController(account_controller)
        self.trivia_controller: TriviaController = TriviaController(account_controller)
