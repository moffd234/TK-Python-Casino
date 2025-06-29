import json
from datetime import datetime, timedelta
from html import unescape

from Application.Model.Games.TriviaGame.Category import Category
from Application.Model.Games.TriviaGame.Question import Question

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


class TriviaGame:

    def __init__(self):
        pass
