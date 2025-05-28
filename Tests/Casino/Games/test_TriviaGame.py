import json
from datetime import datetime
from unittest.mock import patch, mock_open, call, Mock

from requests import HTTPError

from Application.Casino.Accounts.UserAccount import UserAccount
from Application.Casino.Games.TriviaGame.Category import Category
from Application.Casino.Games.TriviaGame.Question import Question
from Application.Casino.Games.TriviaGame.TriviaGame import TriviaGame, create_questions, category_cacher, cache_loader, \
    CACHE_FILE_PATH, parse_cached_categories, main
from Tests.BaseTest import BaseTest, IOCONSOLE_PATH, TRIVIA_GAME_FILE_PATH, TRIVIA_GAME_CLASS_PATH


class TestTriviaGame(BaseTest):

    def setUp(self):
        super().setUp()
        self.game = TriviaGame(self.account, self.manager)
        self.test_question_tf = Question("is this how to spell true 'true'?", "true", ["false"])
        self.test_question_mc = Question("What is the first letter of the alphabet'?",
                                         "a", ["b", "c", "d"])
        self.valid_cats: list[Category] = [
            Category(id_num=9, name='General Knowledge', easy_num=155, med_num=135, hard_num=62),
            Category(id_num=11, name='Entertainment: Film', easy_num=96, med_num=128, hard_num=49),
            Category(id_num=12, name='Entertainment: Music', easy_num=115, med_num=212, hard_num=78),
            Category(id_num=14, name='Entertainment: Television', easy_num=72, med_num=85, hard_num=30),
            Category(id_num=15, name='Entertainment: Video Games', easy_num=365, med_num=497, hard_num=212),
            Category(id_num=17, name='Science & Nature', easy_num=68, med_num=110, hard_num=73),
            Category(id_num=18, name='Science: Computers', easy_num=54, med_num=76, hard_num=40),
            Category(id_num=21, name='Sports', easy_num=53, med_num=68, hard_num=24),
            Category(id_num=22, name='Geography', easy_num=82, med_num=144, hard_num=56),
            Category(id_num=23, name='History', easy_num=78, med_num=177, hard_num=86),
            Category(id_num=31, name='Entertainment: Japanese Anime & Manga', easy_num=62, med_num=84, hard_num=47),
        ]

    @patch(f"{IOCONSOLE_PATH}.print_colored")
    def test_print_welcome(self, mock_print):
        expected: str = r'''
        
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
        '''
        self.game.print_welcome_message()

        mock_print.assert_called_once_with(expected)

    def test_get_winnings_total_hard_multiple(self):
        self.game.q_type = "multiple"
        self.game.difficulty = "hard"
        wager: float = 50.0

        expected: float = 109.38
        actual: float = self.game.get_winnings_total(wager)

        self.assertEqual(expected, actual)

    def test_get_winnings_total_hard_tf(self):
        self.game.q_type = "boolean"
        self.game.difficulty = "hard"
        wager: float = 50.0

        expected: float = 87.5
        actual: float = self.game.get_winnings_total(wager)

        self.assertEqual(expected, actual)

    def test_get_winnings_total_medium_multiple(self):
        self.game.q_type = "multiple"
        self.game.difficulty = "medium"
        wager: float = 50.0

        expected: float = 93.75
        actual: float = self.game.get_winnings_total(wager)

        self.assertEqual(expected, actual)

    def test_get_winnings_total_medium_tf(self):
        self.game.q_type = "boolean"
        self.game.difficulty = "medium"
        wager: float = 50.0

        expected: float = 75.0
        actual: float = self.game.get_winnings_total(wager)

        self.assertEqual(expected, actual)

    def test_get_winnings_total_easy_multiple(self):
        self.game.q_type = "multiple"
        self.game.difficulty = "easy"
        wager: float = 50.0

        expected: float = 78.12
        actual: float = self.game.get_winnings_total(wager)

        self.assertEqual(expected, actual)

    def test_get_winnings_total_easy_tf(self):
        self.game.q_type = "boolean"
        self.game.difficulty = "easy"
        wager: float = 50.0

        expected: float = 62.50
        actual: float = self.game.get_winnings_total(wager)

        self.assertEqual(expected, actual)

    def test_check_answer_tf_true(self):
        self.game.score = 0
        self.game.check_answer("true", self.test_question_tf, 1)

        expected: int = 1
        actual = self.game.score

        self.assertEqual(expected, actual)

    def test_check_answer_mc_right(self):
        self.game.score = 0
        self.game.check_answer("a", self.test_question_mc, 1)

        expected: int = 1
        actual = self.game.score

        self.assertEqual(expected, actual)

    def test_check_answer_mc_wrong(self):
        self.game.score = 0
        self.game.check_answer("c", self.test_question_mc, 1)

        expected: int = 0
        actual = self.game.score

        self.assertEqual(expected, actual)

    def test_create_questions_mc(self):
        response = {'response_code': 0, 'results': [
            {'category': 'Entertainment: Japanese Anime &amp; Manga', 'correct_answer': 'The Porygon Line',
             'difficulty': 'easy', 'incorrect_answers': ['The Pikachu Line', 'The Elekid Line', 'The Magby Line'],
             'question': 'Which Pok&eacute;mon and it&#039;s evolutions were banned from appearing in a main role after the Episode 38 Incident?',
             'type': 'multiple'},
            {'category': 'Entertainment: Japanese Anime &amp; Manga', 'correct_answer': 'Caterpie',
             'difficulty': 'easy', 'incorrect_answers': ['Charmander', 'Pikachu', 'Pidgey'],
             'question': 'What was Ash Ketchum&#039;s second Pokemon?', 'type': 'multiple'},
            {'category': 'Entertainment: Japanese Anime &amp; Manga', 'correct_answer': 'God', 'difficulty': 'easy',
             'incorrect_answers': ['Alien', 'Time Traveler', 'Esper'],
             'question': 'In &quot;The Melancholy of Haruhi Suzumiya&quot; series, the SOS Brigade club leader is unknowingly treated as a(n) __ by her peers.',
             'type': 'multiple'},
            {'category': 'Entertainment: Japanese Anime &amp; Manga', 'correct_answer': 'Manaphy', 'difficulty': 'easy',
             'incorrect_answers': ['Ash', 'May', 'Phantom'],
             'question': 'In the 9th Pokemon movie, who is the Prince of the Sea?', 'type': 'multiple'},
            {'category': 'Entertainment: Japanese Anime &amp; Manga', 'correct_answer': 'Sen (Thousand)',
             'difficulty': 'easy', 'incorrect_answers': ['Hyaku (Hundred)', 'Ichiman (Ten thousand)', 'Juu (Ten)'],
             'question': 'What name is the main character Chihiro given in the 2001 movie &quot;Spirited Away&quot;?',
             'type': 'multiple'},
            {'category': 'Entertainment: Japanese Anime &amp; Manga', 'correct_answer': 'Elizabeth Midford',
             'difficulty': 'easy',
             'incorrect_answers': ['Rachel Phantomhive', 'Alexis Leon Midford', 'Angelina Dalles'],
             'question': 'In the anime Black Butler, who is betrothed to be married to Ciel Phantomhive?',
             'type': 'multiple'},
            {'category': 'Entertainment: Japanese Anime &amp; Manga', 'correct_answer': 'Gainax', 'difficulty': 'easy',
             'incorrect_answers': ['Kyoto Animation', 'Pierrot', 'A-1 Pictures'],
             'question': 'What animation studio produced &quot;Gurren Lagann&quot;?', 'type': 'multiple'},
            {'category': 'Entertainment: Japanese Anime &amp; Manga', 'correct_answer': '8+', 'difficulty': 'easy',
             'incorrect_answers': ['6+', '4+', '5+'],
             'question': 'How many &quot;JoJos&quot; that are protagonists are there in the series &quot;Jojo&#039;s Bizarre Adventure&quot;?',
             'type': 'multiple'},
            {'category': 'Entertainment: Japanese Anime &amp; Manga', 'correct_answer': 'Kaname Chidori',
             'difficulty': 'easy', 'incorrect_answers': ['Teletha Testarossa', 'Melissa Mao', 'Kyoko Tokiwa'],
             'question': 'Who is the main heroine of the anime, Full Metal Panic!', 'type': 'multiple'},
            {'category': 'Entertainment: Japanese Anime &amp; Manga', 'correct_answer': 'Reiner Braun',
             'difficulty': 'easy', 'incorrect_answers': ['Armin Arlelt', 'Mikasa Ackermann', 'Eren Jaeger'],
             'question': 'Who is the armored titan in &quot;Attack On Titan&quot;?', 'type': 'multiple'}]}
        expected_list: list[Question] = [Question(
            question="Which Pokémon and it's evolutions were banned from appearing in a main role after the Episode 38 Incident?",
            answer="The Porygon Line",
            wrong_answers=["The Pikachu Line", "The Elekid Line", "The Magby Line"]),
            Question(
                question="What was Ash Ketchum's second Pokemon?",
                answer="Caterpie",
                wrong_answers=["Charmander", "Pikachu", "Pidgey"]),
            Question(
                question='In "The Melancholy of Haruhi Suzumiya" series, the SOS Brigade club leader is unknowingly treated as a(n) __ by her peers.',
                answer="God",
                wrong_answers=["Alien", "Time Traveler", "Esper"]),
            Question(
                question="In the 9th Pokemon movie, who is the Prince of the Sea?",
                answer="Manaphy",
                wrong_answers=["Ash", "May", "Phantom"]),
            Question(
                question='What name is the main character Chihiro given in the 2001 movie "Spirited Away"?',
                answer="Sen (Thousand)",
                wrong_answers=["Hyaku (Hundred)", "Ichiman (Ten thousand)", "Juu (Ten)"]
            ),
            Question(
                question="In the anime Black Butler, who is betrothed to be married to Ciel Phantomhive?",
                answer="Elizabeth Midford",
                wrong_answers=["Rachel Phantomhive", "Alexis Leon Midford", "Angelina Dalles"]
            ),
            Question(
                question='What animation studio produced "Gurren Lagann"?',
                answer="Gainax",
                wrong_answers=["Kyoto Animation", "Pierrot", "A-1 Pictures"]
            ),
            Question(
                question='How many "JoJos" that are protagonists are there in the series "Jojo\'s Bizarre Adventure"?',
                answer="8+",
                wrong_answers=["6+", "4+", "5+"]
            ),
            Question(
                question="Who is the main heroine of the anime, Full Metal Panic!",
                answer="Kaname Chidori",
                wrong_answers=["Teletha Testarossa", "Melissa Mao", "Kyoko Tokiwa"]
            ),
            Question(
                question='Who is the armored titan in "Attack On Titan"?',
                answer="Reiner Braun",
                wrong_answers=["Armin Arlelt", "Mikasa Ackermann", "Eren Jaeger"]
            )
        ]
        self.assert_create_questions(expected_list, response)

    def test_create_questions_tf(self):
        response = {'response_code': 0, 'results': [
            {'category': 'Entertainment: Film', 'correct_answer': 'False', 'difficulty': 'easy',
             'incorrect_answers': ['True'],
             'question': 'Brandon Routh plays the titular character in the movie &quot;John Wick&quot;.',
             'type': 'boolean'}, {'category': 'Entertainment: Film', 'correct_answer': 'True', 'difficulty': 'easy',
                                  'incorrect_answers': ['False'],
                                  'question': 'Samuel L. Jackson had the words, &#039;Bad Motherf*cker&#039; in-scripted on his lightsaber during the filming of Star Wars.',
                                  'type': 'boolean'},
            {'category': 'Entertainment: Film', 'correct_answer': 'True', 'difficulty': 'easy',
             'incorrect_answers': ['False'],
             'question': 'In the original Star Wars trilogy, David Prowse was the actor who physically portrayed Darth Vader.',
             'type': 'boolean'}, {'category': 'Entertainment: Film', 'correct_answer': 'False', 'difficulty': 'easy',
                                  'incorrect_answers': ['True'],
                                  'question': 'Leonardo DiCaprio won an Oscar for Best Actor in 2004&#039;s &quot;The Aviator&quot;.',
                                  'type': 'boolean'},
            {'category': 'Entertainment: Film', 'correct_answer': 'False', 'difficulty': 'easy',
             'incorrect_answers': ['True'],
             'question': 'Shaquille O&#039;Neal appeared in the 1997 film &quot;Space Jam&quot;.', 'type': 'boolean'},
            {'category': 'Entertainment: Film', 'correct_answer': 'True', 'difficulty': 'easy',
             'incorrect_answers': ['False'],
             'question': 'In the original script of &quot;The Matrix&quot;, the machines used humans as additional computing power instead of batteries.',
             'type': 'boolean'}, {'category': 'Entertainment: Film', 'correct_answer': 'False', 'difficulty': 'easy',
                                  'incorrect_answers': ['True'],
                                  'question': 'Han Solo&#039;s co-pilot and best friend, &quot;Chewbacca&quot;, is an Ewok.',
                                  'type': 'boolean'},
            {'category': 'Entertainment: Film', 'correct_answer': 'True', 'difficulty': 'easy',
             'incorrect_answers': ['False'], 'question': 'Actor Tommy Chong served prison time.', 'type': 'boolean'},
            {'category': 'Entertainment: Film', 'correct_answer': 'False', 'difficulty': 'easy',
             'incorrect_answers': ['True'],
             'question': 'The 2010 film &quot;The Social Network&quot; is a biographical drama film about MySpace founder Tom Anderson.',
             'type': 'boolean'}, {'category': 'Entertainment: Film', 'correct_answer': 'True', 'difficulty': 'easy',
                                  'incorrect_answers': ['False'],
                                  'question': 'The movie &quot;The Nightmare before Christmas&quot; was all done with physical objects.',
                                  'type': 'boolean'}]}
        expected_list: list[Question] = [Question(
            question='Brandon Routh plays the titular character in the movie "John Wick".',
            answer='False',
            wrong_answers=['True']
        ),
            Question(
                question="Samuel L. Jackson had the words, 'Bad Motherf*cker' in-scripted on his lightsaber during the filming of Star Wars.",
                answer='True',
                wrong_answers=['False']
            ),
            Question(
                question='In the original Star Wars trilogy, David Prowse was the actor who physically portrayed Darth Vader.',
                answer='True',
                wrong_answers=['False']
            ),
            Question(
                question='Leonardo DiCaprio won an Oscar for Best Actor in 2004\'s "The Aviator".',
                answer='False',
                wrong_answers=['True']
            ),
            Question(
                question='Shaquille O\'Neal appeared in the 1997 film "Space Jam".',
                answer='False',
                wrong_answers=['True']
            ),
            Question(
                question='In the original script of "The Matrix", the machines used humans as additional computing power instead of batteries.',
                answer='True',
                wrong_answers=['False']
            ),
            Question(
                question='Han Solo\'s co-pilot and best friend, "Chewbacca", is an Ewok.',
                answer='False',
                wrong_answers=['True']
            ),
            Question(
                question='Actor Tommy Chong served prison time.',
                answer='True',
                wrong_answers=['False']
            ),
            Question(
                question='The 2010 film "The Social Network" is a biographical drama film about MySpace founder Tom Anderson.',
                answer='False',
                wrong_answers=['True']
            ),
            Question(
                question='The movie "The Nightmare before Christmas" was all done with physical objects.',
                answer='True',
                wrong_answers=['False']
            )
        ]
        self.assert_create_questions(expected_list, response)

    def assert_create_questions(self, expected_list, response):
        expected_length: int = len(expected_list)
        actual_list: list[Question] = create_questions(response)
        actual_length: int = len(actual_list)

        for i in range(len(expected_list)):
            self.assertEqual(expected_list[i].question, actual_list[i].question)
            self.assertEqual(expected_list[i].answer, actual_list[i].answer)
            self.assertEqual(expected_list[i].wrong_answers, actual_list[i].wrong_answers)
            self.assertEqual(expected_length, actual_length)

    @patch("builtins.open", new_callable=mock_open)
    @patch(f"{TRIVIA_GAME_FILE_PATH}.datetime")
    def test_category_cacher(self, mock_datetime, mock_file):
        mock_datetime.now.return_value = datetime(2025, 4, 11, 12, 0, 0)
        possible_categories: list = [
            Category(id_num=9, name='General Knowledge', easy_num=155, med_num=135, hard_num=62),
            Category(id_num=10, name='Entertainment: Books', easy_num=34, med_num=46, hard_num=28),
            Category(id_num=11, name='Entertainment: Film', easy_num=96, med_num=128, hard_num=49),
            Category(id_num=12, name='Entertainment: Music', easy_num=115, med_num=211, hard_num=78),
            Category(id_num=13, name='Entertainment: Musicals & Theatres', easy_num=10, med_num=14, hard_num=11),
            Category(id_num=14, name='Entertainment: Television', easy_num=72, med_num=85, hard_num=30),
            Category(id_num=15, name='Entertainment: Video Games', easy_num=365, med_num=497, hard_num=212),
            Category(id_num=16, name='Entertainment: Board Games', easy_num=24, med_num=22, hard_num=25),
            Category(id_num=17, name='Science & Nature', easy_num=68, med_num=110, hard_num=73),
            Category(id_num=18, name='Science: Computers', easy_num=54, med_num=76, hard_num=40),
            Category(id_num=19, name='Science: Mathematics', easy_num=16, med_num=26, hard_num=18),
            Category(id_num=20, name='Mythology', easy_num=22, med_num=29, hard_num=14),
            Category(id_num=21, name='Sports', easy_num=53, med_num=68, hard_num=24),
            Category(id_num=22, name='Geography', easy_num=82, med_num=144, hard_num=56),
            Category(id_num=23, name='History', easy_num=78, med_num=177, hard_num=86),
            Category(id_num=24, name='Politics', easy_num=19, med_num=29, hard_num=16),
            Category(id_num=25, name='Art', easy_num=17, med_num=13, hard_num=11),
            Category(id_num=26, name='Celebrities', easy_num=13, med_num=33, hard_num=8),
            Category(id_num=27, name='Animals', easy_num=29, med_num=36, hard_num=18),
            Category(id_num=28, name='Vehicles', easy_num=22, med_num=34, hard_num=20),
            Category(id_num=29, name='Entertainment: Comics', easy_num=16, med_num=39, hard_num=19),
            Category(id_num=30, name='Science: Gadgets', easy_num=15, med_num=10, hard_num=6),
            Category(id_num=31, name='Entertainment: Japanese Anime & Manga', easy_num=62, med_num=84, hard_num=47),
            Category(id_num=32, name='Entertainment: Cartoon & Animations', easy_num=35, med_num=44, hard_num=21)]
        expected = {
            "timestamp": "2025-04-11 12:00:00",
            "categories": [cat.__dict__ for cat in possible_categories]
        }

        category_cacher(possible_categories)

        handle = mock_file()
        written_data = "".join(call.args[0] for call in handle.write.call_args_list)
        actual = json.loads(written_data)

        self.assertEqual(actual, expected)

        mock_file().write.assert_called()

    @patch("os.path.exists", return_value=False)
    def test_cache_loader_no_file(self, mock_path_exists):
        expected: None = cache_loader()
        self.assertIsNone(expected)

    @patch(f"{TRIVIA_GAME_FILE_PATH}.datetime")
    @patch("json.load")
    @patch("builtins.open", new_callable=mock_open)
    @patch("os.path.exists", return_value=True)
    def test_cache_loader_valid(self, mock_path_exists, mock_file, mock_json_load, mock_datetime):
        current_time = datetime(2025, 4, 11, 12, 0, 0)

        mock_datetime.now.return_value = current_time
        mock_datetime.strptime = datetime.strptime

        mock_json_load.return_value = {
            "timestamp": "2025-04-11 10:00:00",
            "categories": [{"id": 1, "name": "Test"}]
        }

        result: dict = cache_loader()

        self.assertEqual(result, [{"id": 1, "name": "Test"}])
        mock_file.assert_called_with(CACHE_FILE_PATH, mode='r')

    def test_parse_cached_categories(self):
        cached_categories = [
            {'easy_num': 155, 'hard_num': 62, 'id': 9, 'med_num': 135, 'name': 'General Knowledge'},
            {'easy_num': 34, 'hard_num': 28, 'id': 10, 'med_num': 46, 'name': 'Entertainment: Books'},
            {'easy_num': 96, 'hard_num': 49, 'id': 11, 'med_num': 128, 'name': 'Entertainment: Film'},
            {'easy_num': 115, 'hard_num': 78, 'id': 12, 'med_num': 212, 'name': 'Entertainment: Music'},
            {'easy_num': 10, 'hard_num': 11, 'id': 13, 'med_num': 14, 'name': 'Entertainment: Musicals & Theatres'},
            {'easy_num': 72, 'hard_num': 30, 'id': 14, 'med_num': 85, 'name': 'Entertainment: Television'},
            {'easy_num': 365, 'hard_num': 212, 'id': 15, 'med_num': 497, 'name': 'Entertainment: Video Games'},
            {'easy_num': 24, 'hard_num': 25, 'id': 16, 'med_num': 22, 'name': 'Entertainment: Board Games'},
            {'easy_num': 68, 'hard_num': 73, 'id': 17, 'med_num': 110, 'name': 'Science & Nature'},
            {'easy_num': 54, 'hard_num': 40, 'id': 18, 'med_num': 76, 'name': 'Science: Computers'},
            {'easy_num': 16, 'hard_num': 18, 'id': 19, 'med_num': 26, 'name': 'Science: Mathematics'},
            {'easy_num': 22, 'hard_num': 14, 'id': 20, 'med_num': 29, 'name': 'Mythology'},
            {'easy_num': 53, 'hard_num': 24, 'id': 21, 'med_num': 68, 'name': 'Sports'},
            {'easy_num': 82, 'hard_num': 56, 'id': 22, 'med_num': 144, 'name': 'Geography'},
            {'easy_num': 78, 'hard_num': 86, 'id': 23, 'med_num': 177, 'name': 'History'},
            {'easy_num': 19, 'hard_num': 17, 'id': 24, 'med_num': 29, 'name': 'Politics'},
            {'easy_num': 17, 'hard_num': 11, 'id': 25, 'med_num': 13, 'name': 'Art'},
            {'easy_num': 13, 'hard_num': 8, 'id': 26, 'med_num': 33, 'name': 'Celebrities'},
            {'easy_num': 29, 'hard_num': 18, 'id': 27, 'med_num': 36, 'name': 'Animals'},
            {'easy_num': 22, 'hard_num': 20, 'id': 28, 'med_num': 34, 'name': 'Vehicles'},
            {'easy_num': 16, 'hard_num': 19, 'id': 29, 'med_num': 39, 'name': 'Entertainment: Comics'},
            {'easy_num': 15, 'hard_num': 6, 'id': 30, 'med_num': 10, 'name': 'Science: Gadgets'},
            {'easy_num': 62, 'hard_num': 47, 'id': 31, 'med_num': 84, 'name': 'Entertainment: Japanese Anime & Manga'},
            {'easy_num': 35, 'hard_num': 21, 'id': 32, 'med_num': 44, 'name': 'Entertainment: Cartoon & Animations'}]
        expected_list: list[Category] = [
            Category(id_num=9, name='General Knowledge', easy_num=155, med_num=135, hard_num=62),
            Category(id_num=10, name='Entertainment: Books', easy_num=34, med_num=46, hard_num=28),
            Category(id_num=11, name='Entertainment: Film', easy_num=96, med_num=128, hard_num=49),
            Category(id_num=12, name='Entertainment: Music', easy_num=115, med_num=212, hard_num=78),
            Category(id_num=13, name='Entertainment: Musicals & Theatres', easy_num=10, med_num=14, hard_num=11),
            Category(id_num=14, name='Entertainment: Television', easy_num=72, med_num=85, hard_num=30),
            Category(id_num=15, name='Entertainment: Video Games', easy_num=365, med_num=497, hard_num=212),
            Category(id_num=16, name='Entertainment: Board Games', easy_num=24, med_num=22, hard_num=25),
            Category(id_num=17, name='Science & Nature', easy_num=68, med_num=110, hard_num=73),
            Category(id_num=18, name='Science: Computers', easy_num=54, med_num=76, hard_num=40),
            Category(id_num=19, name='Science: Mathematics', easy_num=16, med_num=26, hard_num=18),
            Category(id_num=20, name='Mythology', easy_num=22, med_num=29, hard_num=14),
            Category(id_num=21, name='Sports', easy_num=53, med_num=68, hard_num=24),
            Category(id_num=22, name='Geography', easy_num=82, med_num=144, hard_num=56),
            Category(id_num=23, name='History', easy_num=78, med_num=177, hard_num=86),
            Category(id_num=24, name='Politics', easy_num=19, med_num=29, hard_num=17),
            Category(id_num=25, name='Art', easy_num=17, med_num=13, hard_num=11),
            Category(id_num=26, name='Celebrities', easy_num=13, med_num=33, hard_num=8),
            Category(id_num=27, name='Animals', easy_num=29, med_num=36, hard_num=18),
            Category(id_num=28, name='Vehicles', easy_num=22, med_num=34, hard_num=20),
            Category(id_num=29, name='Entertainment: Comics', easy_num=16, med_num=39, hard_num=19),
            Category(id_num=30, name='Science: Gadgets', easy_num=15, med_num=10, hard_num=6),
            Category(id_num=31, name='Entertainment: Japanese Anime & Manga', easy_num=62, med_num=84, hard_num=47),
            Category(id_num=32, name='Entertainment: Cartoon & Animations', easy_num=35, med_num=44, hard_num=21),
        ]
        expected_length: int = len(expected_list)
        actual_list: list[Category] = parse_cached_categories(cached_categories)
        actual_length: int = len(actual_list)

        for i in range(expected_length):
            self.assertEqual(expected_list[i].id, actual_list[i].id)
            self.assertEqual(expected_list[i].name, actual_list[i].name)
            self.assertEqual(expected_list[i].easy_num, actual_list[i].easy_num)
            self.assertEqual(expected_list[i].med_num, actual_list[i].med_num)
            self.assertEqual(expected_list[i].hard_num, actual_list[i].hard_num)

        self.assertEqual(expected_length, actual_length)

    @patch(f"{IOCONSOLE_PATH}.get_string_input", return_value="mc")
    def test_get_question_type_valid_mc(self, mock_input):
        expected: str = "multiple"
        actual: str = self.game.get_question_type()

        self.assertEqual(expected, actual)

    @patch(f"{IOCONSOLE_PATH}.get_string_input", return_value="tf")
    def test_get_question_type_valid_tf(self, mock_input):
        expected: str = "boolean"
        actual: str = self.game.get_question_type()

        self.assertEqual(expected, actual)

    @patch(f"{IOCONSOLE_PATH}.get_string_input", side_effect=["invalid input", "mc"])
    @patch(f"{IOCONSOLE_PATH}.print_error")
    def test_get_question_type_invalid_mc(self, mock_print, mock_input):
        expected: str = "multiple"
        actual: str = self.game.get_question_type()

        mock_print.assert_called_once_with("Invalid input. Please enter either 'mc' or 'tf'")
        mock_input.assert_has_calls([
            call("Enter the type of questions you want to play "
                 "(for multiple choice enter mc "
                 "for true or false enter tf): "),
            call("Enter the type of questions you want to play ")
        ])
        self.assertEqual(expected, actual)

    @patch(f"{IOCONSOLE_PATH}.get_string_input", side_effect=["invalid input", "tf"])
    @patch(f"{IOCONSOLE_PATH}.print_error")
    def test_get_question_type_invalid_tf(self, mock_print, mock_input):
        expected: str = "boolean"
        actual: str = self.game.get_question_type()

        mock_print.assert_called_once_with("Invalid input. Please enter either 'mc' or 'tf'")
        mock_input.assert_has_calls([
            call("Enter the type of questions you want to play "
                 "(for multiple choice enter mc "
                 "for true or false enter tf): "),
            call("Enter the type of questions you want to play ")
        ])
        self.assertEqual(expected, actual)

    @patch(f"{IOCONSOLE_PATH}.get_string_input", return_value="easy")
    def test_get_difficulty_easy(self, mock_input):
        expected: str = "easy"
        actual: str = self.game.get_difficulty()

        self.assertEqual(expected, actual)

    @patch(f"{IOCONSOLE_PATH}.get_string_input", return_value="medium")
    def test_get_difficulty_med(self, mock_input):
        expected: str = "medium"
        actual: str = self.game.get_difficulty()

        self.assertEqual(expected, actual)

    @patch(f"{IOCONSOLE_PATH}.get_string_input", return_value="hard")
    def test_get_difficulty_hard(self, mock_input):
        expected: str = "hard"
        actual: str = self.game.get_difficulty()

        self.assertEqual(expected, actual)

    @patch(f"{IOCONSOLE_PATH}.get_string_input", side_effect=["invalid_input", "easy"])
    @patch(f"{IOCONSOLE_PATH}.print_error")
    def test_get_difficulty_invalid_easy(self, mock_print, mock_input):
        expected: str = "easy"
        actual: str = self.game.get_difficulty()

        mock_print.assert_called_once_with("Invalid input. Please enter either 'easy', 'medium', or 'hard'")
        mock_input.assert_has_calls([
            call("Enter the difficulty you want to play (easy, medium, hard): "),
            call("Enter the difficulty you want to play ")
        ])

        self.assertEqual(expected, actual)

    @patch(f"{IOCONSOLE_PATH}.get_string_input", side_effect=["invalid_input", "medium"])
    @patch(f"{IOCONSOLE_PATH}.print_error")
    def test_get_difficulty_invalid_medium(self, mock_print, mock_input):
        expected: str = "medium"
        actual: str = self.game.get_difficulty()

        mock_print.assert_called_once_with("Invalid input. Please enter either 'easy', 'medium', or 'hard'")
        mock_input.assert_has_calls([
            call("Enter the difficulty you want to play (easy, medium, hard): "),
            call("Enter the difficulty you want to play ")
        ])

        self.assertEqual(expected, actual)

    @patch(f"{IOCONSOLE_PATH}.get_string_input", side_effect=["invalid_input", "hard"])
    @patch(f"{IOCONSOLE_PATH}.print_error")
    def test_get_difficulty_invalid_hard(self, mock_print, mock_input):
        expected: str = "hard"
        actual: str = self.game.get_difficulty()

        mock_print.assert_called_once_with("Invalid input. Please enter either 'easy', 'medium', or 'hard'")
        mock_input.assert_has_calls([
            call("Enter the difficulty you want to play (easy, medium, hard): "),
            call("Enter the difficulty you want to play ")
        ])

        self.assertEqual(expected, actual)

    @patch(f"{IOCONSOLE_PATH}.print_colored")
    @patch(f"{IOCONSOLE_PATH}.get_integer_input", return_value=0)
    def test_get_category_valid(self, mock_input, mock_print_colored):
        expected: Category = self.valid_cats[0]
        actual: Category = self.game.get_category(self.valid_cats)

        self.assert_get_category(expected, actual, mock_print_colored)

    @patch(f"{IOCONSOLE_PATH}.print_colored")
    @patch(f"{IOCONSOLE_PATH}.get_integer_input", return_value=10)
    def test_get_category_valid_upper_bound(self, mock_input, mock_print_colored):
        expected: Category = self.valid_cats[len(self.valid_cats) - 1]
        actual: Category = self.game.get_category(self.valid_cats)

        self.assert_get_category(expected, actual, mock_print_colored)

    @patch(f"{IOCONSOLE_PATH}.print_colored")
    @patch(f"{IOCONSOLE_PATH}.print_error")
    @patch(f"{IOCONSOLE_PATH}.get_integer_input", side_effect=[100, 0])
    def test_get_category_invalid_0(self, mock_input, mock_print_error, mock_print_colored):
        expected: Category = self.valid_cats[0]
        actual: Category = self.game.get_category(self.valid_cats)

        mock_print_error.assert_called_once_with("Invalid category number")

        self.assert_get_category(expected, actual, mock_print_colored)

    @patch(f"{IOCONSOLE_PATH}.print_colored")
    @patch(f"{IOCONSOLE_PATH}.print_error")
    @patch(f"{IOCONSOLE_PATH}.get_integer_input", side_effect=[100, 10])
    def test_get_category_invalid_upper_bound(self, mock_input, mock_print_error, mock_print_colored):
        expected: Category = self.valid_cats[len(self.valid_cats) - 1]
        actual: Category = self.game.get_category(self.valid_cats)

        mock_print_error.assert_called_once_with("Invalid category number")

        self.assert_get_category(expected, actual, mock_print_colored)

    def assert_get_category(self, expected, actual, mock_print_colored):
        expected_print_count: int = len(self.valid_cats) + 2  # Additional print for get_integer and blank print

        mock_print_colored.assert_has_calls([
            call("0. General Knowledge"),
            call("1. Entertainment: Film"),
            call('2. Entertainment: Music'),
            call('3. Entertainment: Television'),
            call('4. Entertainment: Video Games'),
            call('5. Science & Nature'),
            call('6. Science: Computers'),
            call('7. Sports'),
            call('8. Geography'),
            call('9. History'),
            call('10. Entertainment: Japanese Anime & Manga')
        ])

        self.assertEqual(expected, actual)

    @patch(f"{TRIVIA_GAME_CLASS_PATH}.get_question_type", return_value="tf")
    @patch(f"{TRIVIA_GAME_CLASS_PATH}.get_difficulty", return_value="easy")
    @patch(f"{TRIVIA_GAME_CLASS_PATH}.get_category",
           return_value=Category(id_num=9, name='General Knowledge', easy_num=155, med_num=135, hard_num=62))
    @patch(f"{TRIVIA_GAME_CLASS_PATH}.get_valid_categories")
    def test_get_choices(self, mock_valid_cats, mock_cat, mock_diff, mock_type):
        expected_type: str = "tf"
        expected_diff: str = "easy"
        expected_cat: Category = Category(id_num=9, name='General Knowledge', easy_num=155, med_num=135, hard_num=62)

        self.game.get_choices()

        actual_type: str = self.game.q_type
        actual_diff: str = self.game.difficulty
        actual_cat: Category = self.game.cat

        mock_valid_cats.assert_called_once_with(expected_diff)

        self.assertEqual(expected_type, actual_type)
        self.assertEqual(expected_diff, actual_diff)
        self.assert_category_info(expected_cat, actual_cat)

    @patch(f"{TRIVIA_GAME_FILE_PATH}.cache_loader")
    def test_get_possible_categories_cached(self, mock_loader):
        mock_loader.return_value = [
            {"name": "General Knowledge", "id": 9, "easy_num": 152, "med_num": 135, "hard_num": 62}]

        expected: list[Category] = [Category("General Knowledge", 9, 152, 135, 62)]
        expected_len: int = len(expected)
        actual: list[Category] = self.game.get_possible_categories()
        actual_len: int = len(actual)

        self.assertEqual(expected_len, actual_len)
        self.assertEqual(expected[0].name, actual[0].name)
        self.assertEqual(expected[0].id, actual[0].id)
        self.assertEqual(expected[0].easy_num, actual[0].easy_num)
        self.assertEqual(expected[0].med_num, actual[0].med_num)
        self.assertEqual(expected[0].hard_num, actual[0].hard_num)

    @patch(f"{TRIVIA_GAME_FILE_PATH}.cache_loader", return_value=None)
    @patch(f"{TRIVIA_GAME_CLASS_PATH}.get_response", return_value=None)
    @patch(f"{IOCONSOLE_PATH}.print_colored")
    @patch(f"{IOCONSOLE_PATH}.print_error")
    def test_get_possible_categories_no_response(self, mock_print_error, mock_print_colored, mock_response,
                                                 mock_loader):
        outcome: None = self.game.get_possible_categories()

        mock_print_colored.assert_called_with("loading.........\n\n\n")
        mock_response.assert_called_with(f"{self.game.base_url}api_category.php")
        mock_print_error.assert_called_with("Problem getting questions. Please try again later.")

        self.assertIsNone(outcome)

    @patch(f"{TRIVIA_GAME_FILE_PATH}.cache_loader", return_value=None)
    @patch(f"{TRIVIA_GAME_FILE_PATH}.category_cacher")
    @patch(f"{TRIVIA_GAME_CLASS_PATH}.get_response")
    @patch(f"{IOCONSOLE_PATH}.print_colored")
    def test_get_possible_categories_no_cache_valid_response(self, mock_print, mock_response, mock_cacher, mock_loader):
        mock_response.side_effect = [
            {'trivia_categories': [{'id': 9, 'name': 'General Knowledge'},
                                   {'id': 10, 'name': 'Entertainment: Books'},
                                   {'id': 11, 'name': 'Entertainment: Film'}]},
            {'category_id': 9,
             'category_question_count': {'total_easy_question_count': 161, 'total_hard_question_count': 62,
                                         'total_medium_question_count': 142, 'total_question_count': 365}},
            {'category_id': 10,
             'category_question_count': {'total_easy_question_count': 34, 'total_hard_question_count': 29,
                                         'total_medium_question_count': 48, 'total_question_count': 111}},
            {'category_id': 11,
             'category_question_count': {'total_easy_question_count': 99, 'total_hard_question_count': 49,
                                         'total_medium_question_count': 129, 'total_question_count': 277}}
        ]

        expected: list[Category] = [
            Category("General Knowledge", 9, 161, 142, 62),
            Category("Entertainment: Books", 10, 34, 48, 29),
            Category("Entertainment: Film", 11, 99, 129, 49)
        ]
        expected_len: int = len(expected)

        actual: list[Category] = self.game.get_possible_categories()
        actual_len: int = len(actual)

        mock_print.assert_called_with("loading.........\n\n\n")
        mock_cacher.assert_called_with(actual)

        self.assertEqual(expected_len, actual_len)

        for i in range(len(expected)):
            self.assert_category_info(expected[i], actual[i])

    def assert_category_info(self, expected, actual):
        self.assertEqual(expected.name, actual.name)
        self.assertEqual(expected.id, actual.id)
        self.assertEqual(expected.easy_num, actual.easy_num)
        self.assertEqual(expected.med_num, actual.med_num)
        self.assertEqual(expected.hard_num, actual.hard_num)

    @patch(f"{TRIVIA_GAME_CLASS_PATH}.get_possible_categories")
    def test_get_valid_categories_easy(self, mock_get_possible_cats):
        mock_get_possible_cats.return_value = [
            Category("General Knowledge", 9, 161, 142, 62),
            Category("Entertainment: Books", 10, 34, 48, 29),
            Category("Entertainment: Film", 11, 99, 129, 49)
        ]

        expected: list[Category] = [mock_get_possible_cats.return_value[0], mock_get_possible_cats.return_value[2]]
        actual: list[Category] = self.game.get_valid_categories("easy")

        self.assertEqual(expected, actual)

    @patch(f"{TRIVIA_GAME_CLASS_PATH}.get_possible_categories")
    def test_get_valid_categories_medium(self, mock_get_possible_cats):
        mock_get_possible_cats.return_value = [
            Category("General Knowledge", 9, 161, 142, 62),
            Category("Entertainment: Books", 10, 34, 148, 29),
            Category("Entertainment: Film", 11, 99, 29, 49)
        ]

        expected: list[Category] = [mock_get_possible_cats.return_value[0], mock_get_possible_cats.return_value[1]]
        actual: list[Category] = self.game.get_valid_categories("medium")

        self.assertEqual(expected, actual)

    @patch(f"{TRIVIA_GAME_CLASS_PATH}.get_possible_categories")
    def test_get_valid_categories_hard(self, mock_get_possible_cats):
        mock_get_possible_cats.return_value = [
            Category("General Knowledge", 9, 161, 142, 12),
            Category("Entertainment: Books", 10, 34, 148, 29),
            Category("Entertainment: Film", 11, 99, 29, 59)
        ]

        expected: list[Category] = [mock_get_possible_cats.return_value[2]]
        actual: list[Category] = self.game.get_valid_categories("hard")

        self.assertEqual(expected, actual)

    @patch(f"{TRIVIA_GAME_CLASS_PATH}.get_possible_categories")
    def test_get_valid_categories_easy_no_valid(self, mock_get_possible_cats):
        mock_get_possible_cats.return_value = [
            Category("General Knowledge", 9, 1, 1, 12),
            Category("Entertainment: Books", 10, 34, 1, 29),
            Category("Entertainment: Film", 11, 19, 29, 19)
        ]

        expected: list[Category] = []
        actual: list[Category] = self.game.get_valid_categories("easy")

        self.assertEqual(expected, actual)

    @patch(f"{TRIVIA_GAME_CLASS_PATH}.get_possible_categories")
    def test_get_valid_categories_medium_no_valid(self, mock_get_possible_cats):
        mock_get_possible_cats.return_value = [
            Category("General Knowledge", 9, 161, 1, 12),
            Category("Entertainment: Books", 10, 34, 1, 29),
            Category("Entertainment: Film", 11, 19, 29, 19)
        ]

        expected: list[Category] = []
        actual: list[Category] = self.game.get_valid_categories("medium")

        self.assertEqual(expected, actual)

    @patch(f"{TRIVIA_GAME_CLASS_PATH}.get_possible_categories")
    def test_get_valid_categories_hard_no_valid(self, mock_get_possible_cats):
        mock_get_possible_cats.return_value = [
            Category("General Knowledge", 9, 161, 142, 12),
            Category("Entertainment: Books", 10, 34, 148, 29),
            Category("Entertainment: Film", 11, 19, 29, 19)
        ]

        expected: list[Category] = []
        actual: list[Category] = self.game.get_valid_categories("hard")

        self.assertEqual(expected, actual)

    @patch(f"{TRIVIA_GAME_FILE_PATH}.requests.get")
    def test_get_response_success(self, mock_get):
        mock_response = Mock()
        mock_response.raise_for_status.return_value = None
        mock_response.json.return_value = {"results": []}
        mock_get.return_value = mock_response

        result = self.game.get_response("https://test_url.com")

        self.assertEqual(result, {"results": []})
        mock_response.raise_for_status.assert_called_once()
        mock_response.json.assert_called_once()

    @patch(f"{TRIVIA_GAME_FILE_PATH}.requests.get")
    @patch(f"{IOCONSOLE_PATH}.print_error")
    def test_get_response_http_error(self, mock_print, mock_get):
        mock_response = Mock()
        mock_response.raise_for_status.side_effect = HTTPError("Test HTTP Error")
        mock_get.return_value = mock_response

        result = self.game.get_response("https://test_url.com")

        mock_print.assert_called_once_with("Problem getting questions. Please try again later.")
        self.assertIsNone(result)

    @patch(f"{TRIVIA_GAME_FILE_PATH}.os.remove")
    @patch(f"{TRIVIA_GAME_FILE_PATH}.os.path.exists", return_value=True)
    @patch(f"{TRIVIA_GAME_CLASS_PATH}.run")
    def test_main(self, mock_run, mock_exists, mock_remove):
        main()

        mock_run.assert_called_once()
        mock_exists.assert_called_once_with("casino.db")
        mock_remove.assert_called_once_with("casino.db")