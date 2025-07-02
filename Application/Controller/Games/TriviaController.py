from Application.Controller.AccountController import AccountController
from Application.Model.Games.TriviaGame.Category import Category
from Application.Model.Games.TriviaGame.TriviaGame import TriviaGame


class TriviaController:

    def __init__(self, account_controller: AccountController):
        self.account_controller: AccountController = account_controller
        self.game: TriviaGame | None = None

    def setup_game(self, q_type: str, diff: str) -> list[Category]:
        """
        Initializes a new TriviaGame instance with the given question type and difficulty,
        then returns a list of valid trivia categories based on the selected difficulty.

        :param q_type: Question type ("boolean" or "multiple").
        :param diff: Difficulty level ("easy", "medium", or "hard").
        :return: A list of Category objects that are valid for the selected difficulty.
        """
        self.game = TriviaGame(q_type, diff)
        return self.game.get_valid_categories(self.game.difficulty)
