import random


class Question:
    def __init__(self, question: str, answer: str, wrong_answers: list[str]):
        self.question: str = question
        self.answer: str = answer
        self.wrong_answers: list[str] = wrong_answers
        self.all_options: list[str] = self.wrong_answers + [self.answer]
        random.shuffle(self.all_options)
