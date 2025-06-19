from unittest.mock import patch

from Application.Model.Games.CoinFlip.CoinFlip import CoinFlip, handle_heads_tails
from Tests.BaseTest import BaseTest, COINFLIP_FILE_PATH


class TestCoinFlip(BaseTest):

    def setUp(self):
        super().setUp()
        self.game: CoinFlip = CoinFlip()

    @patch(f"{COINFLIP_FILE_PATH}.random.randint", return_value=0)
    def test_handle_heads_tails_zero(self, mock_randint):
        expected: str = "tails"
        actual: str = handle_heads_tails()

        self.assertEqual(expected, actual)

    @patch(f"{COINFLIP_FILE_PATH}.random.randint", return_value=1)
    def test_handle_heads_tails_one(self, mock_randint):
        expected: str = "heads"
        actual: str = handle_heads_tails()

        self.assertEqual(expected, actual)

    @patch("builtins.input", return_value="tails")
    def test_get_guess_tails(self, mock_input):
        expected: str = "tails"
        actual: str = self.game.get_guess()

        self.assertEqual(expected, actual)

    @patch("builtins.input", return_value="heads")
    def test_get_guess_heads(self, mock_input):
        expected: str = "heads"
        actual: str = self.game.get_guess()

        self.assertEqual(expected, actual)

    @patch("builtins.input", side_effect=["invalid_input", "tails"])
    def test_get_guess_invalid_tails(self, mock_input):
        expected: str = "tails"
        actual: str = self.game.get_guess()

        self.assertEqual(expected, actual)

    @patch("builtins.input", side_effect=["invalid_input", "heads"])
    def test_get_guess_invalid_heads(self, mock_input):
        expected: str = "heads"
        actual: str = self.game.get_guess()

        self.assertEqual(expected, actual)

    def test_handle_outcome_win_tails(self):
        expected_output: str = "You Won! The coin was tails"

        actual_output: str = self.game.handle_outcome("tails", "tails", 10)

        self.assertEqual(expected_output, actual_output)

    def test_handle_outcome_win_heads(self):
        expected_output: str = "You Won! The coin was heads"

        actual_output: str = self.game.handle_outcome("heads", "heads", 10)

        self.assertEqual(expected_output, actual_output)

    def test_handle_outcome_loss_tails_guess(self):
        expected_output: str = "You Loss! The coin was heads"
        expected_balance: float = self.account.balance

        actual_output: str = self.game.handle_outcome("tails", "heads", 10)
        actual_balance: float = self.account.balance

        self.assertEqual(expected_output, actual_output)
        self.assertEqual(expected_balance, actual_balance)

    def test_handle_outcome_loss_heads_guess(self):
        expected_output: str = "You Loss! The coin was tails"
        expected_balance: float = self.account.balance

        actual_output: str = self.game.handle_outcome("heads", "tails", 10)
        actual_balance: float = self.account.balance

        self.assertEqual(expected_output, actual_output)
        self.assertEqual(expected_balance, actual_balance)
