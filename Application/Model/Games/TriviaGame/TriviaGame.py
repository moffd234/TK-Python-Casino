from html import unescape

from Application.Model.Games.TriviaGame.Question import Question


def create_questions(q_response: dict) -> list[Question]:
    questions_list: list[Question] = []
    for question in q_response["results"]:
        questions_list.append(Question(question=unescape(question["question"]),
                                       answer=unescape(question["correct_answer"]),
                                       wrong_answers=[unescape(answer) for answer in question["incorrect_answers"]]
                                       ))
    return questions_list


class TriviaGame:

    def __init__(self):
        pass
