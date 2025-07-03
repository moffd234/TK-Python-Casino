import json
import logging
import os
from datetime import datetime, timedelta
from html import unescape

import requests

from Application.Model.Games.TriviaGame.Category import Category
from Application.Model.Games.TriviaGame.Question import Question

CACHE_FILE_PATH = "category_cache.txt"
BASE_URL: str = "https://opentdb.com/"


def category_cacher(categories: list[Category]) -> None:
    """
    Caches a list of trivia categories along with a timestamp to the cache file.

    :param categories: List of Category objects to cache.
    :return: None
    """
    cache: dict = {"timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                   "categories": [cat.__dict__ for cat in categories]}

    with open(CACHE_FILE_PATH, mode='w') as cache_file:
        json.dump(cache, cache_file, indent=4)


def cache_loader() -> dict | None:
    """
    Loads cached trivia categories from a local file if the cache is valid (less than 24 hours old).

    :return: Dictionary of cached categories or None if cache is expired or missing.
    """
    if os.path.exists(CACHE_FILE_PATH):
        with open(CACHE_FILE_PATH, mode='r') as cache_file:
            cache = json.load(cache_file)

            cache_date = datetime.strptime(cache["timestamp"], "%Y-%m-%d %H:%M:%S")
            if datetime.now() - cache_date < timedelta(hours=24):
                return cache["categories"]

    return None


def parse_cached_categories(cache) -> list[Category]:
    """
    Converts cached dictionary data into a list of Category objects.

    :param cache: Cached category data loaded from file.
    :return: List of Category objects.
    """
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


def get_response(url: str) -> None | dict:
    """
    Sends an HTTP GET request to the provided URL and returns the parsed JSON response.

    :param url: The API endpoint to query.
    :return: A dictionary containing the JSON response if successful, or None if the request fails.
    """
    response = requests.get(url)
    try:
        response.raise_for_status()
    except requests.exceptions.HTTPError:
        logging.error(f"HTTP Error when attempting to get_response from {url}")
        return None
    return response.json()


class TriviaGame:

    def __init__(self, q_type: str, difficulty: str):
        self.q_type: str = q_type
        self.difficulty: str = difficulty
        self.cat: Category | None = None
        self.score = 0

    @staticmethod
    def get_possible_categories() -> list[Category] | None:
        """
        Retrieves a list of trivia categories from cache if available and valid,
        or from the OpenTDB API otherwise. Caches the result for future use.

        :return: A list of Category objects if successful, or None if the API call fails.
        """
        cached_categories: dict | None = cache_loader()

        if cached_categories:
            return parse_cached_categories(cached_categories)

        cat_response = get_response(f"{BASE_URL}api_category.php")

        if cat_response is None:
            logging.error("Unable to get any response from Trivia Game's Category API")
            return None

        all_categories: dict = {category["name"]: category["id"] for category in cat_response["trivia_categories"]}
        possible_categories: list[Category] = []

        for key, value in all_categories.items():
            response = get_response(f"{BASE_URL}api_count.php?category={value}")

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

    def create_questions(self) -> list[Question] | None:
        """
        Parses a JSON response from the trivia API and constructs a list of Question objects.

        :return: A list of Question objects.
        """
        response: dict | None = self.get_question_response()

        if not response:
            logging.error(f"Issue getting questions for difficulty: {self.difficulty}, and category: {self.cat}")
            return None

        questions_list: list[Question] = []
        for question in response["results"]:
            questions_list.append(Question(question=unescape(question["question"]),
                                           answer=unescape(question["correct_answer"]),
                                           wrong_answers=[unescape(answer) for answer in question["incorrect_answers"]]
                                           ))
        return questions_list

    def get_question_response(self) -> dict | None:
        """
        Builds and sends a request to the OpenTDB API to retrieve 10 trivia questions
        based on the configured category, difficulty, and question type.

        :return: A dictionary containing the API response with trivia questions, or None if the request fails.
        """
        url: str = (f"{BASE_URL}api.php?amount=10&category={self.cat.id}"
                    f"&difficulty={self.difficulty}&type={self.q_type}")

        return get_response(url)

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

    def check_answer(self, answer: str, question: Question) -> bool:
        """
        Compares the user's answer to the correct answer for a given question.
        Increments the score if the answer is correct.

        :param answer: The user's submitted answer.
        :param question: The Question object containing the correct answer.
        :return: True if the user's answer is correct; False otherwise.
        """
        if answer.lower().strip() == question.answer.lower().strip():
            self.score += 1
            return True

        return False

    def get_winnings_total(self, wager: float) -> float:
        """
        Calculates the user's total winnings based on the selected question type,
        difficulty level, and wager amount.

        :param wager: The amount of money wagered by the user.
        :return: The calculated winnings, rounded to two decimal places.
        """
        multipliers = {"easy": 1.25, "medium": 1.5, "hard": 1.75, "boolean": 1, "multiple": 1.25}
        multiplier = multipliers[self.difficulty] * multipliers[self.q_type]
        return round(wager * multiplier, 2)
