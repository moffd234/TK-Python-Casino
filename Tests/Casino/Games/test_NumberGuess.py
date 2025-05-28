from unittest.mock import patch

from Application.Casino.Games.NumberGuess.NumberGuess import NumberGuess, main
from Tests.BaseTest import BaseTest, IOCONSOLE_PATH, NUMBERGUESS_FILE_PATH, NUMBERGUESS_CLASS_PATH


class TestNumberGuess(BaseTest):

    def setUp(self):
        super().setUp()
        self.game: NumberGuess = NumberGuess(self.account, self.manager)

    def assert_run(self, mock_get_guess, mock_handle_guess, mock_print, mock_print_welcome, mock_random, mock_wager):
        self.game.run()
        mock_handle_guess.assert_called_once()
        mock_get_guess.assert_called_once()
        mock_random.assert_called_once()
        mock_wager.assert_called_once()
        mock_print_welcome.assert_called_once()

    @patch("builtins.print")
    def test_print_welcome_message(self, mock_print):
        expected: str = r"""[36m
        
        Yb        dP 888888 88      dP""b8  dP"Yb  8b    d8 888888     888888  dP"Yb      88b 88 88   88 8b    d8      dP""b8 88   88 888888 .dP"Y8 .dP"Y8 
         Yb  db  dP  88__   88     dP   `" dP   Yb 88b  d88 88__         88   dP   Yb     88Yb88 88   88 88b  d88     dP   `" 88   88 88__   `Ybo." `Ybo." 
          YbdPYbdP   88""   88  .o Yb      Yb   dP 88YbdP88 88""         88   Yb   dP     88 Y88 Y8   8P 88YbdP88     Yb  "88 Y8   8P 88""   o.`Y8b o.`Y8b 
           YP  YP    888888 88ood8  YboodP  YbodP  88 YY 88 888888       88    YbodP      88  Y8 `YbodP' 88 YY 88      YboodP `YbodP' 888888 8bodP' 8bodP' 
           
           Rules:
                1. A random integer will be generated from 1 to 10 (including 1 and 10)
                2. You will get one chance to input a guess
                3. If you are right you will win 2x your wager
        """
        self.game.print_welcome_message()
        mock_print.assert_called_once_with(expected)

    def test_handle_guess_right(self):
        expected_output: str = "You Won! The answer was 5"
        expected_balance: float = self.account.balance + 20

        actual_output: str = self.game.handle_guess(5, 5, 10)
        actual_balance: float = self.account.balance

        self.assertEqual(expected_output, actual_output)
        self.assertEqual(expected_balance, actual_balance)

    def test_handle_guess_wrong(self):
        expected_output: str = "You lost. The answer was 5"
        expected_balance: float = self.account.balance

        actual_output: str = self.game.handle_guess(6, 5, 10)
        actual_balance: float = self.account.balance

        self.assertEqual(expected_output, actual_output)
        self.assertEqual(expected_balance, actual_balance)

    @patch("builtins.input", return_value="2")
    def test_get_guess_valid(self, mock_input):
        expected: int = 2
        actual: int = self.game.get_guess()

        self.assertEqual(expected, actual)

    @patch("builtins.input", return_value="1")
    def test_get_guess_valid_lower_bound(self, mock_input):
        expected: int = 1
        actual: int = self.game.get_guess()

        self.assertEqual(expected, actual)

    @patch("builtins.input", return_value="1")
    def test_get_guess_valid_upper_bound(self, mock_input):
        expected: int = 1
        actual: int = self.game.get_guess()

        self.assertEqual(expected, actual)

    @patch("builtins.input", side_effect=["11", "5"])
    @patch(f"{IOCONSOLE_PATH}.print_error")
    def test_get_guess_too_high(self, mock_print, mock_input):
        expected: int = 5
        actual: int = self.game.get_guess()

        mock_print.assert_called_with("Number should be from 1 - 10 (inclusive)")
        self.assertEqual(expected, actual)

    @patch("builtins.input", side_effect=["0", "3"])
    @patch(f"{IOCONSOLE_PATH}.print_error")
    def test_get_guess_too_low(self, mock_print, mock_input):
        expected: int = 3
        actual: int = self.game.get_guess()

        mock_print.assert_called_with("Number should be from 1 - 10 (inclusive)")
        self.assertEqual(expected, actual)

    @patch("builtins.input", side_effect=["-1", "4"])
    @patch(f"{IOCONSOLE_PATH}.print_error")
    def test_get_guess_too_negative(self, mock_print, mock_input):
        expected: int = 4
        actual: int = self.game.get_guess()

        mock_print.assert_called_with("Number should be from 1 - 10 (inclusive)")
        self.assertEqual(expected, actual)

    @patch(f"{NUMBERGUESS_CLASS_PATH}.print_welcome_message")
    @patch(f"{NUMBERGUESS_CLASS_PATH}.get_continue_input", side_effect=[True, False])
    @patch(f"{NUMBERGUESS_CLASS_PATH}.get_wager_amount", return_value=10.0)
    @patch(f"{NUMBERGUESS_FILE_PATH}.random.randint", return_value=5)
    @patch(f"{NUMBERGUESS_CLASS_PATH}.get_guess", return_value=5)
    @patch(f"{NUMBERGUESS_CLASS_PATH}.handle_guess", return_value="You Won! The answer was 5")
    @patch(f"{IOCONSOLE_PATH}.print_colored")
    def test_run_once_win(self, mock_print, mock_handle_guess, mock_get_guess, mock_random, mock_wager, mock_continue,
                      mock_print_welcome):
        self.assert_run(mock_get_guess, mock_handle_guess, mock_print, mock_print_welcome, mock_random, mock_wager)
        mock_print.assert_called_once_with(f"You Won! The answer was {mock_random.return_value}")

        expected_call_count: int = 2
        actual_call_count: int = mock_continue.call_count

        self.assertEqual(expected_call_count, actual_call_count)

    @patch(f"{NUMBERGUESS_CLASS_PATH}.print_welcome_message")
    @patch(f"{NUMBERGUESS_CLASS_PATH}.get_continue_input", side_effect=[True, False])
    @patch(f"{NUMBERGUESS_CLASS_PATH}.get_wager_amount", return_value=10.0)
    @patch(f"{NUMBERGUESS_FILE_PATH}.random.randint", return_value=5)
    @patch(f"{NUMBERGUESS_CLASS_PATH}.get_guess", return_value=2)
    @patch(f"{NUMBERGUESS_CLASS_PATH}.handle_guess", return_value="You lost! The answer was 5")
    @patch(f"{IOCONSOLE_PATH}.print_colored")
    def test_run_once_lose(self, mock_print, mock_handle_guess, mock_get_guess, mock_random, mock_wager, mock_continue,
                          mock_print_welcome):
        self.assert_run(mock_get_guess, mock_handle_guess, mock_print, mock_print_welcome, mock_random, mock_wager)
        mock_print.assert_called_once_with(f"You lost! The answer was {mock_random.return_value}")

        expected_call_count: int = 2
        actual_call_count: int = mock_continue.call_count

        self.assertEqual(expected_call_count, actual_call_count)

    @patch(f"{NUMBERGUESS_CLASS_PATH}.print_welcome_message")
    @patch(f"{NUMBERGUESS_CLASS_PATH}.get_continue_input", side_effect=[True, True, False])
    @patch(f"{NUMBERGUESS_CLASS_PATH}.get_wager_amount", return_value=10.0)
    @patch(f"{NUMBERGUESS_FILE_PATH}.random.randint", return_value=5)
    @patch(f"{NUMBERGUESS_CLASS_PATH}.get_guess", return_value=2)
    @patch(f"{NUMBERGUESS_CLASS_PATH}.handle_guess", return_value="You lost! The answer was 5")
    @patch(f"{IOCONSOLE_PATH}.print_colored")
    def test_run_twice(self, mock_print, mock_handle_guess, mock_get_guess, mock_random, mock_wager, mock_continue,
                           mock_print_welcome):


        self.game.run()

        expected_call_count: int = 2
        mock_print_call_count: int = mock_print.call_count
        mock_handle_guess_call_count: int = mock_handle_guess.call_count
        mock_wager_call_count: int = mock_wager.call_count
        mock_print_welcome_calls_count: int = mock_print_welcome.call_count
        mock_get_guess_call_count: int = mock_get_guess.call_count
        mock_random_calls_count: int = mock_random.call_count
        mock_continue_calls_count: int = mock_continue.call_count

        self.assertEqual(expected_call_count, mock_print_call_count)
        self.assertEqual(expected_call_count, mock_handle_guess_call_count)
        self.assertEqual(expected_call_count, mock_wager_call_count)
        self.assertEqual(expected_call_count - 1, mock_print_welcome_calls_count)
        self.assertEqual(expected_call_count, mock_get_guess_call_count)
        self.assertEqual(expected_call_count, mock_random_calls_count)
        self.assertEqual(expected_call_count + 1, mock_continue_calls_count)

    @patch(f"{NUMBERGUESS_FILE_PATH}.os.remove")
    @patch(f"{NUMBERGUESS_FILE_PATH}.os.path.exists", return_value=True)
    @patch(f"{NUMBERGUESS_CLASS_PATH}.run")
    def test_main(self, mock_run, mock_exists, mock_remove):
        main()

        mock_run.assert_called_once()
        mock_exists.assert_called_once_with("casino.db")
        mock_remove.assert_called_once_with("casino.db")