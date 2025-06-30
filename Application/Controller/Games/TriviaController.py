from Application.Controller.AccountController import AccountController
from Application.Model.Games.TriviaGame.Category import Category
from Application.Model.Games.TriviaGame.TriviaGame import TriviaGame


class TriviaController:

    def __init__(self, account_controller: AccountController):
        self.account_controller: AccountController = account_controller
        self.game: TriviaGame | None = None

    def start_game(self, q_type: str, diff: str, cat: Category) -> None:
        """
        Initializes a new TriviaGame instance with the given parameters.

        :param q_type: Question type ("boolean" or "multiple").
        :param diff: Difficulty level ("easy", "medium", "hard").
        :param cat: Selected Category instance.
        """
        self.game = TriviaGame(q_type, diff, cat)
