from unittest.mock import patch

from Application.Casino.Games.CoinFlip.CoinFlip import CoinFlip, handle_heads_tails, main
from Tests.BaseTest import BaseTest, COINFLIP_FILE_PATH, COINFLIP_CLASS_PATH, IOCONSOLE_PATH


class TestCoinFlip(BaseTest):

    def setUp(self):
        super().setUp()
        self.game: CoinFlip = CoinFlip(self.account, self.manager)



    def assert_run(self, mock_continue, mock_guess, mock_heads_tails, mock_input, mock_print, mock_welcome):
        self.game.run()
        mock_welcome.assert_called_once()
        mock_heads_tails.assert_called_once()
        mock_guess.assert_called_once()
        mock_input.assert_called_once()
        mock_print.assert_called_once_with(
            self.game.handle_outcome(mock_guess.return_value, mock_heads_tails.return_value, 10.0))
        expected_call_count: int = 2
        continue_call_count: int = mock_continue.call_count
        self.assertEqual(expected_call_count, continue_call_count)

    @patch("builtins.print")
    def test_print_welcome(self, mock_print):
        expected: str = r"""[34m
        
        Yb        dP 888888 88      dP""b8  dP"Yb  8b    d8 888888     888888  dP"Yb       dP""b8  dP"Yb  88 88b 88     888888 88     88 88""Yb 
         Yb  db  dP  88__   88     dP   `" dP   Yb 88b  d88 88__         88   dP   Yb     dP   `" dP   Yb 88 88Yb88     88__   88     88 88__dP 
          YbdPYbdP   88""   88  .o Yb      Yb   dP 88YbdP88 88""         88   Yb   dP     Yb      Yb   dP 88 88 Y88     88""   88  .o 88 88
           YP  YP    888888 88ood8  YboodP  YbodP  88 YY 88 888888       88    YbodP       YboodP  YbodP  88 88  Y8     88     88ood8 88 88     
        
        rules:
             1. Enter a guess of either heads or tails
             2. A coin will be flipped
             3. If you guess correctly you will win 1.25x your wager
        """
        self.game.print_welcome_message()
        mock_print.assert_called_once_with(expected)

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
        expected_balance: float = self.account.balance + (10 * 1.25)

        actual_output: str = self.game.handle_outcome("tails", "tails", 10)
        actual_balance: float = self.account.balance

        self.assertEqual(expected_output, actual_output)
        self.assertEqual(expected_balance, actual_balance)

    def test_handle_outcome_win_heads(self):
        expected_output: str = "You Won! The coin was heads"
        expected_balance: float = self.account.balance + (10 * 1.25)

        actual_output: str = self.game.handle_outcome("heads", "heads", 10)
        actual_balance: float = self.account.balance

        self.assertEqual(expected_output, actual_output)
        self.assertEqual(expected_balance, actual_balance)

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

    @patch(f"{COINFLIP_CLASS_PATH}.print_welcome_message")
    @patch(f"{COINFLIP_CLASS_PATH}.get_continue_input", side_effect=[True, False])
    @patch(f"{COINFLIP_FILE_PATH}.handle_heads_tails", return_value="tails")
    @patch(f"{COINFLIP_CLASS_PATH}.get_guess", return_value="tails")
    @patch(f"{IOCONSOLE_PATH}.get_monetary_input", return_value=10.0)
    @patch(f"{IOCONSOLE_PATH}.print_colored")
    def test_run_win(self, mock_print, mock_input, mock_guess, mock_heads_tails, mock_continue, mock_welcome):
        self.assert_run(mock_continue, mock_guess, mock_heads_tails, mock_input, mock_print, mock_welcome)

        expected_message = "You Won! The coin was tails"
        mock_print.assert_called_once_with(expected_message)

    @patch(f"{COINFLIP_CLASS_PATH}.print_welcome_message")
    @patch(f"{COINFLIP_CLASS_PATH}.get_continue_input", side_effect=[True, False])
    @patch(f"{COINFLIP_FILE_PATH}.handle_heads_tails", return_value="tails")
    @patch(f"{COINFLIP_CLASS_PATH}.get_guess", return_value="heads")
    @patch(f"{IOCONSOLE_PATH}.get_monetary_input", return_value=10.0)
    @patch(f"{IOCONSOLE_PATH}.print_colored")
    def test_run_lose(self, mock_print, mock_input, mock_guess, mock_heads_tails, mock_continue, mock_welcome):
        self.assert_run(mock_continue, mock_guess, mock_heads_tails, mock_input, mock_print, mock_welcome)

        expected_message = f"You Loss! The coin was tails"
        mock_print.assert_called_once_with(expected_message)

    @patch(f"{COINFLIP_CLASS_PATH}.print_welcome_message")
    @patch(f"{COINFLIP_CLASS_PATH}.get_continue_input", side_effect=[True, True, False])
    @patch(f"{COINFLIP_FILE_PATH}.handle_heads_tails", return_value="tails")
    @patch(f"{COINFLIP_CLASS_PATH}.get_guess", return_value="heads")
    @patch(f"{IOCONSOLE_PATH}.get_monetary_input", return_value=10.0)
    @patch(f"{IOCONSOLE_PATH}.print_colored")
    def test_run_multiple_games(self, mock_print, mock_input, mock_guess, mock_heads_tails, mock_continue, mock_welcome):
        self.game.run()

        expected_call_count: int = 2
        continue_call_count: int = mock_continue.call_count
        heads_tails_call_count: int = mock_heads_tails.call_count
        guess_call_count: int = mock_guess.call_count
        input_call_count: int = mock_input.call_count

        self.assertEqual(expected_call_count + 1, continue_call_count)
        self.assertEqual(heads_tails_call_count, expected_call_count)
        self.assertEqual(guess_call_count, expected_call_count)
        self.assertEqual(input_call_count, expected_call_count)

    @patch(f"{COINFLIP_FILE_PATH}.os.remove")
    @patch(f"{COINFLIP_FILE_PATH}.os.path.exists", return_value=True)
    @patch(f"{COINFLIP_CLASS_PATH}.run")
    def test_main(self, mock_run, mock_exists, mock_remove):
        main()

        mock_run.assert_called_once()
        mock_exists.assert_called_once_with("casino.db")
        mock_remove.assert_called_once_with("casino.db")
