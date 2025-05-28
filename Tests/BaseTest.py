import os.path
import unittest

from Application.Casino.Accounts.AccountManager import AccountManager
from Application.Casino.Accounts.UserAccount import UserAccount
from Application.Casino.Accounts.db import init_db

IOCONSOLE_PATH: str = "Application.Utils.IOConsole.IOConsole"
GAMES_PATH: str = "Application.Casino.Games"
GAME_CLASS_PATH: str = "Application.Casino.Games.Game.Game"
TRIVIA_GAME_FILE_PATH: str = f"{GAMES_PATH}.TriviaGame.TriviaGame"
TRIVIA_GAME_CLASS_PATH: str = f"{TRIVIA_GAME_FILE_PATH}.TriviaGame"
TICTACTOE_FILE_PATH: str = f"{GAMES_PATH}.TicTacToe.TicTacToe"
TICTACTOE_CLASS_PATH: str = f"{TICTACTOE_FILE_PATH}.TicTacToe"
RPS_FILE_PATH: str = f"{GAMES_PATH}.RockPaperScissors.RPS"
RPS_CLASS_PATH: str = f"{RPS_FILE_PATH}.RPS"
SLOTS_FILE_PATH: str = f"{GAMES_PATH}.Slots.Slots"
SLOTS_CLASS_PATH: str = f"{SLOTS_FILE_PATH}.Slots"
COINFLIP_FILE_PATH: str = f"{GAMES_PATH}.CoinFlip.CoinFlip"
COINFLIP_CLASS_PATH: str = f"{COINFLIP_FILE_PATH}.CoinFlip"
NUMBERGUESS_FILE_PATH: str = f"{GAMES_PATH}.NumberGuess.NumberGuess"
NUMBERGUESS_CLASS_PATH: str = f"{NUMBERGUESS_FILE_PATH}.NumberGuess"
CASINO_CLASS_PATH: str = "Application.Casino.Casino.Casino"
USER_ACCOUNT_CLASS_PATH: str = "Application.Casino.Accounts.UserAccount.UserAccount"
ACCOUNT_MANAGER_CLASS_PATH: str = "Application.Casino.Accounts.AccountManager.AccountManager"
TEST_QUESTIONS: list[str] = ["Who is your favorite sports team?", "Test Answer",
                             "What street did you grow up on?", "Test Street"]


class BaseTest(unittest.TestCase):

    def setUp(self):
        self.session = init_db(in_memory=True)
        self.manager = AccountManager(session=self.session)
        self.account = UserAccount("test_username", "ValidPassword123!", 50.0,
                                   "test@email.com", TEST_QUESTIONS)

    def tearDown(self):
        if hasattr(self.manager, 'session'):
            self.manager.session.close()

        if os.path.exists("casino.db"):
            os.remove("casino.db")

        if os.path.exists("category_cache.txt"):
            os.remove("category_cache.txt")
