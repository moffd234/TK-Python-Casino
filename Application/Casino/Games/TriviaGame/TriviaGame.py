from datetime import datetime, timedelta
from html import unescape
import json
import os
import requests

from Application.Casino.Accounts.AccountManager import AccountManager
from Application.Casino.Accounts.UserAccount import UserAccount
from Application.Casino.Games.Game import Game
from Application.Casino.Games.TriviaGame.Category import Category
from Application.Casino.Games.TriviaGame.Question import Question
from Application.Utils.ANSI_COLORS import ANSI_COLORS

CACHE_FILE_PATH = "category_cache.txt"


def create_questions(q_response: dict) -> list[Question]:
    questions_list: list[Question] = []
    for question in q_response["results"]:
        questions_list.append(Question(question=unescape(question["question"]),
                                       answer=unescape(question["correct_answer"]),
                                       wrong_answers=[unescape(answer) for answer in question["incorrect_answers"]]
                                       ))
    return questions_list


def category_cacher(categories: list[Category]) -> None:
    cache: dict = {"timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                   "categories": [cat.__dict__ for cat in categories]}

    with open(CACHE_FILE_PATH, mode='w') as cache_file:
        json.dump(cache, cache_file, indent=4)


def cache_loader() -> dict | None:
    if os.path.exists(CACHE_FILE_PATH):
        with open(CACHE_FILE_PATH, mode='r') as cache_file:
            cache = json.load(cache_file)

            cache_date = datetime.strptime(cache["timestamp"], "%Y-%m-%d %H:%M:%S")
            if datetime.now() - cache_date < timedelta(hours=24):
                return cache["categories"]

    return None


def parse_cached_categories(cache) -> list[Category]:
    possible_categories: list[Category] = []
    for category in cache:
        possible_categories.append(Category(
            name=category.get("name"),
            id_num=category.get("id"),
            easy_num=category.get("easy_num"),
            med_num=category.get("med_num"),
            hard_num=category.get("hard_num"))
        )
    return possible_categories


class TriviaGame(Game):

    def __init__(self, player: UserAccount, manager: AccountManager):
        super().__init__(player, manager)
        self.q_type: str = ""
        self.difficulty: str = ""
        self.cat: Category | None = None
        self.console.color = ANSI_COLORS.GREEN.value
        self.base_url = "https://opentdb.com/"
        self.score = 0

    def print_welcome_message(self) -> None:
        self.console.print_colored(r'''
        
        Yb        dP 888888 88      dP""b8  dP"Yb  8b    d8 888888     888888  dP"Yb      888888 88""Yb 88 Yb    dP 88    db    
         Yb  db  dP  88__   88     dP   `" dP   Yb 88b  d88 88__         88   dP   Yb       88   88__dP 88  Yb  dP  88   dPYb   
          YbdPYbdP   88""   88  .o Yb      Yb   dP 88YbdP88 88""         88   Yb   dP       88   88"Yb  88   YbdP   88  dP__Yb  
           YP  YP    888888 88ood8  YboodP  YbodP  88 YY 88 888888       88    YbodP        88   88  Yb 88    YP    88 dP""""Yb 
        
        Rules:
                1. Select difficulty, category, and the type of questions 
                  -Payout is:
                             1.25x your wager if you choose medium
                             1.5x your wager if you choose hard
                             an additional 1.25x your wager if you choose multiple choice
                2. You will then be given 10 questions from that category
                3. You must answer at least 7 questions correctly to win
        ''')

    def run(self):

        self.print_welcome_message()

        while self.get_continue_input():
            wager: float = self.get_wager_amount()

            self.get_choices()
            url: str = (f"{self.base_url}api.php?amount=10&category={self.cat.id}"
                        f"&difficulty={self.difficulty}&type={self.q_type}")
            response = self.get_response(url)

            questions: list[Question] = create_questions(response)
            self.play_game(questions)

            if self.score > 6:
                winnings = self.get_winnings_total(wager)
                self.manager.add_and_save_account(self.player, winnings)
                self.console.print_colored(f"You Won!!! Your winnings were {winnings}.\n"
                                           f"This brings your account total to {self.player.balance}")
            else:
                self.console.print_colored("Sorry you did not get enough questions correct. "
                                           "Better luck next time")

    def get_question_type(self) -> str:
        question_type: str = self.console.get_string_input("Enter the type of questions you want to play "
                                                           "(for multiple choice enter mc "
                                                           "for true or false enter tf): ")
        while question_type != "mc" and question_type != "tf":
            self.console.print_error("Invalid input. Please enter either 'mc' or 'tf'")
            question_type = self.console.get_string_input("Enter the type of questions you want to play ")

        return "boolean" if question_type == "tf" else "multiple"

    def get_difficulty(self) -> str:
        difficulty: str = self.console.get_string_input("Enter the difficulty you want to play (easy, medium, hard): ")
        while difficulty != "easy" and difficulty != "medium" and difficulty != "hard":
            self.console.print_error("Invalid input. Please enter either 'easy', 'medium', or 'hard'")
            difficulty = self.console.get_string_input("Enter the difficulty you want to play ")

        return difficulty

    def get_category(self, valid_cats: list[Category]) -> Category:
        self.console.print_colored("Available Categories:")
        for i in range(len(valid_cats)):
            self.console.print_colored(f"{i}. {valid_cats[i].name}")

        print()

        choice = -1
        while choice < 0 or choice >= len(valid_cats):
            choice = self.console.get_integer_input("Enter category number")

            if choice < 0 or choice >= len(valid_cats):
                self.console.print_error("Invalid category number")

        return valid_cats[choice]

    def get_choices(self):
        self.q_type = self.get_question_type()
        self.difficulty = self.get_difficulty()

        valid_cats = self.get_valid_categories(self.difficulty)
        self.cat: Category = self.get_category(valid_cats)

    def get_possible_categories(self) -> list[Category] | None:
        cached_categories: dict | None = cache_loader()

        if cached_categories:
            return parse_cached_categories(cached_categories)

        self.console.print_colored("loading.........\n\n\n")
        cat_response = self.get_response(f"{self.base_url}api_category.php")

        if cat_response is None:
            self.console.print_error("Problem getting questions. Please try again later.")
            return None

        all_categories: dict = {category["name"]: category["id"] for category in cat_response["trivia_categories"]}
        possible_categories: list[Category] = []

        for key, value in all_categories.items():
            response = self.get_response(f"{self.base_url}api_count.php?category={value}")

            if response:
                category_data = response.get("category_question_count", {})
                possible_categories.append(Category(
                    name=key,
                    id_num=value,
                    easy_num=category_data.get("total_easy_question_count", 0),
                    med_num=category_data.get("total_medium_question_count", 0),
                    hard_num=category_data.get("total_hard_question_count", 0)
                ))

        category_cacher(possible_categories)
        return possible_categories

    def get_valid_categories(self, difficulty: str) -> list[Category]:
        """

        Iterates through list of Categories and returns a list of only the categories that are valid

        :param difficulty: the chosen difficulty of the questions
        :return: a list of valid categories to use

        Currently, the only way to check a category's question count is the get the count of all questions. However,
        this does not specify how many of those questions are true/false and how many are multiple choice. Thus,
        we must iterate through all the possible categories and see if it has 50+ questions for a given difficulty at
        which point we can assume it has 10+ for both true/false and multiple choice
        """
        categories: list[Category] = self.get_possible_categories()
        valid_categories: list[Category] = []

        for cat in categories:
            if difficulty == "easy" and cat.easy_num >= 50:
                valid_categories.append(cat)

            elif difficulty == "medium" and cat.med_num >= 50:
                valid_categories.append(cat)

            elif difficulty == "hard" and cat.hard_num >= 50:
                valid_categories.append(cat)

        return valid_categories

    def check_answer(self, answer: str, question: Question, question_num) -> None:
        if answer.lower().strip() == question.answer.lower().strip():
            self.score += 1
            print(f"Correct!! Your new score is {self.score}/{question_num}")
        else:
            print(f"Wrong. Current score is {self.score}/{question_num}")

    def play_game(self, questions: list[Question]) -> int:
        for i in range(len(questions)):
            print(questions[i].question)
            options = ' '.join(f"[{answer}]" for answer in questions[i].all_options)

            if len(questions[i].wrong_answers) == 1:  # ASSERT: Must be a true or false question
                guess = str(self.console.get_boolean_input(options))

            else:
                guess = self.console.get_string_input(options)

            self.check_answer(guess, questions[i], i + 1)

        return self.score

    def get_winnings_total(self, wager: float) -> float:
        multipliers = {"easy": 1.25, "medium": 1.5, "hard": 1.75, "boolean": 1, "multiple": 1.25}
        multiplier = multipliers[self.difficulty] * multipliers[self.q_type]
        return round(wager * multiplier, 2)

    def get_response(self, url: str) -> None | dict:
        response = requests.get(url)
        try:
            response.raise_for_status()
        except requests.exceptions.HTTPError:
            self.console.print_error("Problem getting questions. Please try again later.")
            return None
        return response.json()


def main():
    account_manager: AccountManager = AccountManager()
    account: UserAccount = UserAccount("Tester", "ValidPassword123!", 1000, "test@email.com",
                                       ["Who is your favorite sports team?", "Test Answer",
                                        "What street did you grow up on?", "Test Street"])
    game: TriviaGame = TriviaGame(account, account_manager)
    game.run()

    if os.path.exists("casino.db"):
        os.remove("casino.db")


if __name__ == "__main__":
    main()
