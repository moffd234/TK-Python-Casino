from Application.Casino.Accounts.UserAccount import UserAccount
from Tests.BaseTest import BaseTest


class TestUserAccount(BaseTest):

    def setUp(self):
        super().setUp()

    def test_constructor(self):
        self.assertEqual(self.account.username, "test_username")
        self.assertEqual(self.account.password, "ValidPassword123!")
        self.assertEqual(self.account.balance, 50)
        self.assertEqual(self.account.security_question_one, "Who is your favorite sports team?")
        self.assertEqual(self.account.security_question_two, "What street did you grow up on?")
        self.assertEqual(self.account.security_answer_one, "Test Answer")
        self.assertEqual(self.account.security_answer_two, "Test Street")

    def test_subtract_losses(self):
        expected: float = self.account.balance - 10

        self.account.subtract_losses(10)

        self.assertEqual(self.account.balance, expected)

    def test_subtract_losses_negative(self):
        expected: str = "Wager must be positive"
        with self.assertRaises(ValueError) as ve:
            self.account.subtract_losses(-10)

        actual: str = ve.exception.args[0]
        self.assertEqual(expected, actual)

    def test_subtract_losses_negative_balance(self):
        expected: str = f"Insufficient funds! Available: {self.account.balance}, Tried to subtract: {100}"
        with self.assertRaises(ValueError) as ve:
            self.account.subtract_losses(100)

        actual: str = ve.exception.args[0]
        self.assertEqual(expected, actual)

    def test_add_winnings(self):
        expected: float = self.account.balance + 10
        self.account.add_winnings(10)
        actual: float = self.account.balance

        self.assertEqual(expected, actual)

    def test_add_winnings_negative(self):
        with self.assertRaises(ValueError):
            self.account.add_winnings(-10)

    def test_repr(self):
        expected: str = "Username: test_username Balance: 50.0"
        actual: str = self.account.__repr__()
        self.assertEqual(expected, actual)