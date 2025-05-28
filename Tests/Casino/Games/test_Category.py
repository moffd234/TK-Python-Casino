from Application.Casino.Games.TriviaGame.Category import Category
from Tests.BaseTest import BaseTest


class TestCategory(BaseTest):

    def test_category_to_dict(self):
        cat: Category = Category("General Knowledge", 9, 10, 11, 12)

        expected: dict = {"name": "General Knowledge", "id": 9, "easy_num": 10, "med_num": 11, "hard_num": 12}
        actual: dict = cat.to_dict()

        self.assertEqual(expected, actual)