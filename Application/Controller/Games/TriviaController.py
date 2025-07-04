from Application.Controller.AccountController import AccountController
from Application.Model.Games.TriviaGame.Category import Category
from Application.Model.Games.TriviaGame.Question import Question
from Application.Model.Games.TriviaGame.TriviaGame import TriviaGame


class TriviaController:

    def __init__(self, account_controller: AccountController):
        self.account_controller: AccountController = account_controller
        self.game: TriviaGame | None = None
        self.question_list: list[Question] | None = None
        self.question_num: int = 0

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

    def get_question_list(self, cat: Category) -> list[Question] | None:
        """
        Sets the selected trivia category on the current game instance and retrieves a list of questions.

        :param cat: The Category object selected by the user.
        :return: A list of Question objects if retrieval is successful; otherwise, None.
        """
        self.game.set_category(cat)
        self.question_list = self.game.create_questions()

        if self.question_list:
            return self.question_list

        return None

    def check_answer(self, answer: str) -> bool:
        """
        Checks whether the provided answer is correct for the current question.

        Delegates to the TriviaGame's check_answer method and compares the user's input
        against the correct answer for the current question in the question list.

        :param answer: The user's answer to the current trivia question.
        :return: True if the answer is correct, False otherwise.
        """
        self.question_num += 1
        return self.game.check_answer(answer, self.question_list[self.question_num - 1])
