import json
import os
from datetime import datetime, timedelta
from html import unescape

import requests

from Application.Model.Games.TriviaGame.Category import Category
from Application.Model.Games.TriviaGame.Question import Question

CACHE_FILE_PATH = "category_cache.txt"
BASE_URL: str = "https://opentdb.com/"


def create_questions(q_response: dict) -> list[Question]:
    """
    Parses a JSON response from the trivia API and constructs a list of Question objects.

    :param q_response: JSON dictionary containing trivia questions.
    :return: A list of Question objects.
    """
    questions_list: list[Question] = []
    for question in q_response["results"]:
        questions_list.append(Question(question=unescape(question["question"]),
                                       answer=unescape(question["correct_answer"]),
                                       wrong_answers=[unescape(answer) for answer in question["incorrect_answers"]]
                                       ))
    return questions_list


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
    response = requests.get(url)
    try:
        response.raise_for_status()
    except requests.exceptions.HTTPError:
        return None
    return response.json()


def get_possible_categories() -> list[Category] | None:
    cached_categories: dict | None = cache_loader()

    if cached_categories:
        return parse_cached_categories(cached_categories)

    cat_response = get_response(f"{BASE_URL}api_category.php")

    if cat_response is None:
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


class TriviaGame:

    def __init__(self, q_type: str, difficulty: str, cat: Category):
        self.q_type: str = q_type
        self.difficulty: str = difficulty
        self.cat: Category = cat
        self.score = 0
