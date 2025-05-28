from unittest.mock import patch, call

from Application.Casino.Casino import *
from Tests.BaseTest import BaseTest, IOCONSOLE_PATH, COINFLIP_FILE_PATH, GAMES_PATH, SLOTS_FILE_PATH, CASINO_CLASS_PATH, \
    ACCOUNT_MANAGER_CLASS_PATH, TEST_QUESTIONS
from Tests.Casino.Games.test_RPS import RPS_FILE_PATH
from Tests.Casino.Games.test_TicTacToe import TICTACTOE_CLASS_PATH
from Tests.Casino.Games.test_TriviaGame import TRIVIA_GAME_CLASS_PATH


class TestCasino(BaseTest):

    def setUp(self):
        super().setUp()
        self.casino = Casino()
        self.casino.account = self.account

    def assert_prompt_game(self, mock_input, mock_run):
        self.casino.prompt_game()
        mock_input.assert_has_calls([call("Welcome to the Game Selection Dashboard!" +
                                          "\nFrom here, you can select any of the following options:" +
                                          "\n\t[ RPS ], [ NUMBERGUESS ],"
                                          " [ TRIVIA ], [ TIC-TAC-TOE ]. [ COINFLIP ], [ SLOTS ]"),
                                     call("Welcome to the Game Selection Dashboard!" +
                                          "\nFrom here, you can select any of the following options:" +
                                          "\n\t[ RPS ], [ NUMBERGUESS ],"
                                          " [ TRIVIA ], [ TIC-TAC-TOE ]. [ COINFLIP ], [ SLOTS ]")])
        mock_run.assert_called_once()

    def assert_prompt_manage_or_select(self, mock_input, mock_selection):
        self.casino.prompt_manage_or_select()
        mock_input.assert_has_calls([call('You are logged in!\nFrom here, you can select any of the following options:'
                                          '\n\t[ manage-account ], [ select-game ], [ logout ]'),
                                     call('You are logged in!\nFrom here, you can select any of the following options:'
                                          '\n\t[ manage-account ], [ select-game ], [ logout ]')])
        mock_selection.assert_called_once()

    def assert_account_info(self, account, expected_username="test_username", expected_password="ValidPassword123!",
                            hashed_password = None):
        expected_username = expected_username
        expected_password = expected_password
        expected_balance = 50.0
        expected_email = "test@email.com"
        expected_questions = TEST_QUESTIONS
        actual_username = account.username
        actual_password = account.password
        actual_balance = account.balance
        actual_email = account.email
        actual_questions = [account.security_question_one, account.security_answer_one,
                            account.security_question_two, account.security_answer_two]

        self.assertEqual(expected_username, actual_username)
        self.assertEqual(expected_balance, actual_balance)
        self.assertEqual(expected_email, actual_email)
        self.assertEqual(expected_questions, actual_questions)

        if hashed_password:
            actual: bool = verify_password(expected_password, actual_password)
            self.assertTrue(actual)
        else:
            self.assertEqual(expected_password, actual_password)

    @patch("builtins.print")
    def test_print_welcome(self, mock_print):
        expected: str = r"""[34m
            888       888          888                                         888 888 
            888   o   888          888                                         888 888 
            888  d8b  888          888                                         888 888 
            888 d888b 888  .d88b.  888  .d8888b .d88b.  88888b.d88b.   .d88b.  888 888 
            888d88888b888 d8P  Y8b 888 d88P"   d88""88b 888 "888 "88b d8P  Y8b 888 888 
            88888P Y88888 88888888 888 888     888  888 888  888  888 88888888 Y8P Y8P 
            8888P   Y8888 Y8b.     888 Y88b.   Y88..88P 888  888  888 Y8b.      "   "  
            888P     Y888  "Y8888  888  "Y8888P "Y88P"  888  888  888  "Y8888  888 888
            
            Notes:
                - At anypoint you can exit the application by typing "exit"
                - Funds can be added and you can reset you password from the manage account screen after logging in
            """
        self.casino.print_welcome()
        mock_print.assert_called_with(expected)

    @patch(f"{ACCOUNT_MANAGER_CLASS_PATH}.get_account",
           return_value=UserAccount("test_username", "ValidPassword123!", 50.0,
                                    "test@email.com", TEST_QUESTIONS))
    @patch(f"{IOCONSOLE_PATH}.get_string_input", side_effect=["test_username", "ValidPassword123!"])
    def test_handle_login(self, mock_inputs, mock_get_account):
        account: UserAccount = self.casino.handle_login()

        self.assert_account_info(account)

    @patch(f"{ACCOUNT_MANAGER_CLASS_PATH}.get_account", return_value=None)
    @patch(f"{IOCONSOLE_PATH}.get_string_input", side_effect=["wrong_user", "wrong_pass"] * 5)
    def test_handle_login_fail(self, mock_get_string_input, mock_get_account):
        account = self.casino.handle_login()
        self.assertIsNone(account)

    @patch(f"{CASINO_CLASS_PATH}.prompt_username", return_value="test_username")
    @patch(f"{CASINO_CLASS_PATH}.prompt_password", return_value="ValidPassword123!")
    @patch(f"{CASINO_CLASS_PATH}.prompt_email", return_value="test@email.com")
    @patch(f"{CASINO_CLASS_PATH}.get_security_questions_and_answers", return_value=TEST_QUESTIONS)
    def test_handle_signup(self, mock_questions, mock_email, mock_password, mock_username):
        account: UserAccount = self.casino.handle_signup()
        self.assert_account_info(account, hashed_password=mock_password.return_value)

    @patch(f"{IOCONSOLE_PATH}.print_error")
    @patch(f"{ACCOUNT_MANAGER_CLASS_PATH}.create_account",
           side_effect=[None, UserAccount("test_username", "ValidPassword123!", 50.0,
                                          "test@email.com", TEST_QUESTIONS)])
    @patch(f"{CASINO_CLASS_PATH}.prompt_username", return_value="test_username")
    @patch(f"{CASINO_CLASS_PATH}.prompt_password", return_value="ValidPassword123!")
    @patch(f"{CASINO_CLASS_PATH}.prompt_email", return_value="test@email.com")
    @patch(f"{CASINO_CLASS_PATH}.get_security_questions_and_answers", return_value=TEST_QUESTIONS)
    def test_handle_signup_account_exist(self, mock_questions, mock_create_account, mock_email,
                                         mock_password, mock_username, mock_print):
        account: UserAccount = self.casino.handle_signup()

        mock_print.assert_called_once_with("Account with that username already exists")

        self.assert_account_info(account)

    @patch("builtins.print")
    @patch("builtins.input", return_value="50")
    def test_handle_add_funds(self, mock_input, mock_print):
        expected_balance: float = self.casino.account.balance + 50
        self.casino.add_funds()

        actual_balance: float = self.casino.account.balance

        mock_print.assert_called_once_with(f"{ANSI_COLORS.GREEN.value}You have added $50.0 to your funds!"
                                           f" New Balance is {self.casino.account.balance}")
        self.assertEqual(expected_balance, actual_balance)

    @patch(f"{IOCONSOLE_PATH}.print_colored")
    @patch("builtins.input", side_effect=["-1", "50"])
    def test_handle_add_funds_negative(self, mock_input, mock_print):
        self.add_funds_and_assert(mock_print)

    @patch(f"{IOCONSOLE_PATH}.print_colored")
    @patch("builtins.input", side_effect=[".99", "50"])
    def test_handle_add_funds_low_decimal(self, mock_input, mock_print):
        self.add_funds_and_assert(mock_print)

    def add_funds_and_assert(self, mock_print):
        expected_balance: float = self.casino.account.balance + 50
        self.casino.add_funds()
        actual_balance: float = self.casino.account.balance
        mock_print.assert_has_calls([
            call("Please enter a valid amount "
                 "(A positive number >= 1.00 with no more than 2 decimal places).",
                 ANSI_COLORS.RED),
            call(
                f"You have added $50.0 to your funds! New Balance is {self.casino.account.balance}", ANSI_COLORS.GREEN)
        ])
        self.assertEqual(expected_balance, actual_balance)

    @patch(f"{IOCONSOLE_PATH}.print_colored")
    @patch(f"{IOCONSOLE_PATH}.get_string_input", side_effect=["ValidPassword123!", "NewValidPassword123!"])
    def test_reset_password(self, mock_input, mock_print):
        self.casino.account = self.manager.create_account("test_username", "ValidPassword123!",
                                                   "email@test_domain.com", TEST_QUESTIONS)
        was_successful: bool = self.casino.reset_password()

        expected_password = "NewValidPassword123!"
        actual_password = self.casino.account.password

        actual: bool = verify_password(expected_password, actual_password)

        mock_print.assert_called_once_with("Your password has been updated!", ANSI_COLORS.GREEN)
        self.assertTrue(actual)
        self.assertTrue(was_successful)

    @patch(f"{CASINO_CLASS_PATH}.update_password")
    @patch("builtins.input", side_effect=["ValidPassword123!", "NewValidPassword123!"])
    def test_reset_password_assert_update_called(self, mock_input, mock_update_password):
        self.casino.account = self.manager.create_account("test_username", "ValidPassword123!",
                                                          "email@test_domain.com", TEST_QUESTIONS)
        was_successful: bool = self.casino.reset_password()

        expected_password = "NewValidPassword123!"

        mock_update_password.assert_called_once_with()
        self.assertTrue(was_successful)

    @patch(f"{IOCONSOLE_PATH}.print_colored")
    @patch("builtins.input", side_effect=["test_pAsSwOrD123!", "ValidPassword123!"])
    def test_reset_password_case_sensitive(self, mock_input, mock_print):
        account: UserAccount = self.casino.manager.create_account("test_username", "test_pAsSwOrD123!",
                                                                  "email@domain.com", TEST_QUESTIONS)
        self.casino.account = account
        was_successful: bool = self.casino.reset_password()

        expected_password = "ValidPassword123!"
        actual_password = self.casino.account.password

        actual: bool = verify_password(expected_password, actual_password)

        mock_print.assert_called_once_with(f"Your password has been updated!", ANSI_COLORS.GREEN)
        self.assertTrue(actual)
        self.assertTrue(was_successful)

    @patch(f"{IOCONSOLE_PATH}.print_error")
    @patch("builtins.input", side_effect=["wrong_password"] * 5)
    def test_reset_password_failed_times(self, mock_input, mock_print_error):
        self.casino.account = self.manager.create_account("test_username", "ValidPassword123!",
                                                          "email@test_domain.com", TEST_QUESTIONS)
        expected_password: str = self.casino.account.password
        was_successful: bool = self.casino.reset_password()

        actual_password = self.casino.account.password

        # 5 incorrect password messages and 1 lockout message
        mock_print_error.assert_has_calls([
            call("Passwords do not match"),
            call("Passwords do not match"),
            call("Passwords do not match"),
            call("Passwords do not match"),
            call("Passwords do not match"),
            call("Too many invalid attempts. Please try again")
        ])
        self.assertEqual(expected_password, actual_password)
        self.assertFalse(was_successful)

    @patch(f"{IOCONSOLE_PATH}.print_colored")
    @patch(f"{IOCONSOLE_PATH}.print_error")
    @patch("builtins.input",
           side_effect=["wrong_password", "wrong_password", "ValidPassword123!", "NewValidPassword123!"])
    def test_reset_password_failed_then_works(self, mock_input, mock_print_error, mock_print):
        self.casino.account = self.manager.create_account("test_username", "ValidPassword123!",
                                                          "email@test_domain.com", TEST_QUESTIONS)
        was_successful: bool = self.casino.reset_password()

        expected_password: str = "NewValidPassword123!"
        actual_password = self.casino.account.password
        actual: bool = verify_password(expected_password, actual_password)

        mock_print.assert_called_once_with("Your password has been updated!", ANSI_COLORS.GREEN)
        mock_print_error.assert_has_calls([
            call("Passwords do not match"),
            call("Passwords do not match")
        ])
        self.assertTrue(actual)
        self.assertTrue(was_successful)

    @patch(f"{CASINO_CLASS_PATH}.add_funds")
    @patch("builtins.input", return_value="add")
    def test_handle_manage_selection_add(self, mock_input, mock_add_funds):
        self.casino.handle_manage_selection()
        mock_add_funds.assert_called_once()

    @patch(f"{CASINO_CLASS_PATH}.add_funds")
    @patch("builtins.input", return_value="add-funds")
    def test_handle_manage_selection_add_dash_funds(self, mock_input, mock_add_funds):
        self.casino.handle_manage_selection()
        mock_add_funds.assert_called_once()

    @patch(f"{CASINO_CLASS_PATH}.add_funds")
    @patch("builtins.input", return_value="add funds")
    def test_handle_manage_selection_add_funds(self, mock_input, mock_add_funds):
        self.casino.handle_manage_selection()
        mock_add_funds.assert_called_once()

    @patch(f"{CASINO_CLASS_PATH}.reset_password")
    @patch("builtins.input", return_value="reset")
    def test_handle_manage_selection_reset(self, mock_input, mock_reset):
        self.casino.handle_manage_selection()
        mock_reset.assert_called_once()

    @patch(f"{CASINO_CLASS_PATH}.reset_password")
    @patch("builtins.input", return_value="reset password")
    def test_handle_manage_selection_reset_password(self, mock_input, mock_reset):
        self.casino.handle_manage_selection()
        mock_reset.assert_called_once()

    @patch(f"{CASINO_CLASS_PATH}.reset_password")
    @patch("builtins.input", return_value="reset-password")
    def test_handle_manage_selection_reset_dash_password(self, mock_input, mock_reset):
        self.casino.handle_manage_selection()
        mock_reset.assert_called_once()

    @patch("builtins.input", return_value="back")
    def test_handle_manage_selection_back(self, mock_input):
        result: None = self.casino.handle_manage_selection()
        self.assertIsNone(result)

    @patch("builtins.input", return_value="go back")
    def test_handle_manage_selection_go_back(self, mock_input):
        result: None = self.casino.handle_manage_selection()
        self.assertIsNone(result)

    @patch("builtins.input", return_value="go-back")
    def test_handle_manage_selection_go_dash_back(self, mock_input):
        result: None = self.casino.handle_manage_selection()
        self.assertIsNone(result)

    @patch(f"{IOCONSOLE_PATH}.print_error")
    @patch(f"{CASINO_CLASS_PATH}.add_funds")
    @patch("builtins.input", side_effect=["invalid_input", "add"])
    def test_handle_manage_selection_invalid_input(self, mock_input, mock_add, mock_print):
        self.casino.handle_manage_selection()
        mock_print.assert_called_once_with("Invalid input. Please try again")
        mock_add.assert_called_once()

    @patch("builtins.input", return_value="login")
    @patch(f"{CASINO_CLASS_PATH}.handle_login",
           return_value=UserAccount("test_username", "ValidPassword123!", 50,
                                    "test@email.com", TEST_QUESTIONS))
    def test_handle_initial_action_login(self, mock_login, mock_input):
        actual_account: UserAccount | None = self.casino.handle_initial_action()
        self.assert_account_info(actual_account)

    @patch("builtins.input", return_value="signup")
    @patch(f"{CASINO_CLASS_PATH}.handle_signup",
           return_value=UserAccount("test_username", "ValidPassword123!", 50,
                                    "test@email.com", TEST_QUESTIONS))
    def test_handle_initial_action_signup(self, mock_signup, mock_input):
        actual_account: UserAccount | None = self.casino.handle_initial_action()
        self.assert_account_info(actual_account, "test_username", "ValidPassword123!")

    @patch("builtins.input", side_effect=["invalid_input", "signup"])
    @patch(f"{CASINO_CLASS_PATH}.handle_signup",
           return_value=UserAccount("test_username", "ValidPassword123!", 50,
                                    "test@email.com", TEST_QUESTIONS))
    @patch(f"{IOCONSOLE_PATH}.print_error")
    def test_handle_initial_action_invalid_then_signup(self, mock_print, mock_signup, mock_input):
        actual_account: UserAccount | None = self.casino.handle_initial_action()

        mock_print.assert_called_once_with("Invalid input. Please try again\n\n")
        self.assert_account_info(actual_account, "test_username", "ValidPassword123!")

    @patch("builtins.input", side_effect=["invalid_input", "login"])
    @patch(f"{CASINO_CLASS_PATH}.handle_login",
           return_value=UserAccount("test_username", "ValidPassword123!", 50,
                                    "test@email.com", TEST_QUESTIONS))
    @patch(f"{IOCONSOLE_PATH}.print_error")
    def test_handle_initial_action_login_with_invalid(self, mock_print, mock_login, mock_input):
        actual_account: UserAccount | None = self.casino.handle_initial_action()

        mock_print.assert_called_once_with("Invalid input. Please try again\n\n")
        self.assert_account_info(actual_account)

    @patch("builtins.input", side_effect=["reset", "login"])
    @patch(f"{CASINO_CLASS_PATH}.reset_from_login")
    @patch(f"{CASINO_CLASS_PATH}.handle_login",
           return_value=UserAccount("test_username", "ValidPassword123!", 50,
                                    "test@email.com", TEST_QUESTIONS))
    def test_handle_initial_action_reset_then_login(self, mock_login, mock_reset, mock_input):
        actual_account: UserAccount = self.casino.handle_initial_action()

        mock_login.assert_called_once()
        mock_reset.assert_called_once()

        self.assert_account_info(actual_account)

    @patch("builtins.input", side_effect=["reset", "signup"])
    @patch(f"{CASINO_CLASS_PATH}.reset_from_login")
    @patch(f"{CASINO_CLASS_PATH}.handle_signup",
           return_value=UserAccount("test_username", "ValidPassword123!", 50,
                                    "test@email.com", TEST_QUESTIONS))
    def test_handle_initial_action_reset_then_signup(self, mock_login, mock_reset, mock_input):
        actual_account: UserAccount = self.casino.handle_initial_action()

        mock_login.assert_called_once()
        mock_reset.assert_called_once()

        self.assert_account_info(actual_account)

    @patch(f"{IOCONSOLE_PATH}.get_string_input", side_effect=["manage", "logout"])
    @patch(f"{CASINO_CLASS_PATH}.handle_manage_selection")
    def test_prompt_manage_or_select_manage(self, mock_selection, mock_input):
        self.assert_prompt_manage_or_select(mock_input, mock_selection)

    @patch(f"{IOCONSOLE_PATH}.get_string_input", side_effect=["manage account", "logout"])
    @patch(f"{CASINO_CLASS_PATH}.handle_manage_selection")
    def test_prompt_manage_or_select_manage_account(self, mock_selection, mock_input):
        self.assert_prompt_manage_or_select(mock_input, mock_selection)

    @patch(f"{IOCONSOLE_PATH}.get_string_input", side_effect=["manage-account", "logout"])
    @patch(f"{CASINO_CLASS_PATH}.handle_manage_selection")
    def test_prompt_manage_or_select_manage_dash_account(self, mock_selection, mock_input):
        self.assert_prompt_manage_or_select(mock_input, mock_selection)

    @patch(f"{IOCONSOLE_PATH}.get_string_input", side_effect=["select", "logout"])
    @patch(f"{CASINO_CLASS_PATH}.prompt_game")
    def test_prompt_manage_or_select_select(self, mock_selection, mock_input):
        self.assert_prompt_manage_or_select(mock_input, mock_selection)

    @patch(f"{IOCONSOLE_PATH}.get_string_input", side_effect=["select game", "logout"])
    @patch(f"{CASINO_CLASS_PATH}.prompt_game")
    def test_prompt_manage_or_select_select_game(self, mock_selection, mock_input):
        self.assert_prompt_manage_or_select(mock_input, mock_selection)

    @patch(f"{IOCONSOLE_PATH}.get_string_input", side_effect=["select game", "logout"])
    @patch(f"{IOCONSOLE_PATH}.print_error")
    @patch(f"{CASINO_CLASS_PATH}.prompt_game")
    def test_prompt_manage_or_select_select_game_invalid_funds(self, mock_selection, mock_print, mock_input):
        self.casino.account.balance = 0.00
        self.casino.prompt_manage_or_select()
        mock_input.assert_has_calls([call('You are logged in!\nFrom here, you can select any of the following options:'
                                          '\n\t[ manage-account ], [ select-game ], [ logout ]'),
                                     call('You are logged in!\nFrom here, you can select any of the following options:'
                                          '\n\t[ manage-account ], [ select-game ], [ logout ]')])

    @patch(f"{IOCONSOLE_PATH}.get_string_input", side_effect=["select-game", "logout"])
    @patch(f"{CASINO_CLASS_PATH}.prompt_game")
    def test_prompt_manage_or_select_select_dash_game(self, mock_selection, mock_input):
        self.assert_prompt_manage_or_select(mock_input, mock_selection)

    @patch(f"{IOCONSOLE_PATH}.get_string_input", side_effect=["logout"])
    def test_prompt_manage_or_select_logout(self, mock_input):
        self.assertIsNone(self.casino.prompt_manage_or_select())
        mock_input.assert_called_once_with('You are logged in!\nFrom here, you can select any of the following options:'
                                           '\n\t[ manage-account ], [ select-game ], [ logout ]')

    @patch(f"{IOCONSOLE_PATH}.get_string_input", side_effect=["invalid_input", "logout"])
    @patch(f"{IOCONSOLE_PATH}.print_error")
    def test_prompt_manage_or_select_invalid_input(self, mock_print, mock_input):
        self.casino.prompt_manage_or_select()
        mock_input.assert_has_calls([call('You are logged in!\nFrom here, you can select any of the following options:'
                                          '\n\t[ manage-account ], [ select-game ], [ logout ]'),
                                     call('You are logged in!\nFrom here, you can select any of the following options:'
                                          '\n\t[ manage-account ], [ select-game ], [ logout ]')])

        mock_print.assert_called_once_with("Invalid input. Please try again\n\n")

    @patch(f"{IOCONSOLE_PATH}.get_string_input", side_effect=["rps", "back"])
    @patch(f"{RPS_FILE_PATH}.RPS.run", return_value=None)
    def test_prompt_game_rps(self, mock_run, mock_input):
        self.assert_prompt_game(mock_input, mock_run)

    @patch(f"{IOCONSOLE_PATH}.get_string_input", side_effect=["rock paper scissors", "back"])
    @patch(f"{RPS_FILE_PATH}.RPS.run", return_value=None)
    def test_prompt_game_rock_paper_scissors(self, mock_run, mock_input):
        self.assert_prompt_game(mock_input, mock_run)

    @patch(f"{IOCONSOLE_PATH}.get_string_input", side_effect=["numberguess", "back"])
    @patch(f"{GAMES_PATH}.NumberGuess.NumberGuess.NumberGuess.run", return_value=None)
    def test_prompt_game_numberguess(self, mock_run, mock_input):
        self.assert_prompt_game(mock_input, mock_run)

    @patch(f"{IOCONSOLE_PATH}.get_string_input", side_effect=["number guess", "back"])
    @patch(f"{GAMES_PATH}.NumberGuess.NumberGuess.NumberGuess.run", return_value=None)
    def test_prompt_game_number_guess(self, mock_run, mock_input):
        self.assert_prompt_game(mock_input, mock_run)

    @patch(f"{IOCONSOLE_PATH}.get_string_input", side_effect=["trivia", "back"])
    @patch(f"{TRIVIA_GAME_CLASS_PATH}.run", return_value=None)
    def test_prompt_game_trivia(self, mock_run, mock_input):
        self.assert_prompt_game(mock_input, mock_run)

    @patch(f"{IOCONSOLE_PATH}.get_string_input", side_effect=["tic-tac-toe", "back"])
    @patch(f"{TICTACTOE_CLASS_PATH}.run", return_value=None)
    def test_prompt_game_tic_tac_toe_dashes(self, mock_run, mock_input):
        self.assert_prompt_game(mock_input, mock_run)

    @patch(f"{IOCONSOLE_PATH}.get_string_input", side_effect=["tictactoe", "back"])
    @patch(f"{TICTACTOE_CLASS_PATH}.run", return_value=None)
    def test_prompt_game_tictactoe(self, mock_run, mock_input):
        self.assert_prompt_game(mock_input, mock_run)

    @patch(f"{IOCONSOLE_PATH}.get_string_input", side_effect=["coinflip", "back"])
    @patch(f"{COINFLIP_FILE_PATH}.CoinFlip.run", return_value=None)
    def test_prompt_game_coinflip(self, mock_run, mock_input):
        self.assert_prompt_game(mock_input, mock_run)

    @patch(f"{IOCONSOLE_PATH}.get_string_input", side_effect=["coin flip", "back"])
    @patch(f"{COINFLIP_FILE_PATH}.CoinFlip.run", return_value=None)
    def test_prompt_game_coin_flip(self, mock_run, mock_input):
        self.assert_prompt_game(mock_input, mock_run)

    @patch(f"{IOCONSOLE_PATH}.get_string_input", side_effect=["slots", "back"])
    @patch(f"{SLOTS_FILE_PATH}.Slots.run", return_value=None)
    def test_prompt_game_slots(self, mock_run, mock_input):
        self.assert_prompt_game(mock_input, mock_run)

    @patch(f"{IOCONSOLE_PATH}.get_string_input", return_value="back")
    def test_prompt_game_back(self, mock_input):
        self.casino.prompt_game()
        mock_input.assert_called_once_with("Welcome to the Game Selection Dashboard!" +
                                           "\nFrom here, you can select any of the following options:" +
                                           "\n\t[ RPS ], [ NUMBERGUESS ],"
                                           " [ TRIVIA ], [ TIC-TAC-TOE ]. [ COINFLIP ], [ SLOTS ]")

    @patch(f"{IOCONSOLE_PATH}.get_string_input", side_effect=["invalid_input",
                                                              "coin flip", "back"])
    @patch(f"{COINFLIP_FILE_PATH}.CoinFlip.run", return_value=None)
    @patch(f"{IOCONSOLE_PATH}.print_error")
    def test_prompt_game_invalid_input(self, mock_print, mock_run, mock_input):
        self.casino.prompt_game()
        mock_input.assert_has_calls([call("Welcome to the Game Selection Dashboard!" +
                                          "\nFrom here, you can select any of the following options:" +
                                          "\n\t[ RPS ], [ NUMBERGUESS ],"
                                          " [ TRIVIA ], [ TIC-TAC-TOE ]. [ COINFLIP ], [ SLOTS ]"),
                                     call("Welcome to the Game Selection Dashboard!" +
                                          "\nFrom here, you can select any of the following options:" +
                                          "\n\t[ RPS ], [ NUMBERGUESS ],"
                                          " [ TRIVIA ], [ TIC-TAC-TOE ]. [ COINFLIP ], [ SLOTS ]"),
                                     call("Welcome to the Game Selection Dashboard!" +
                                          "\nFrom here, you can select any of the following options:" +
                                          "\n\t[ RPS ], [ NUMBERGUESS ],"
                                          " [ TRIVIA ], [ TIC-TAC-TOE ]. [ COINFLIP ], [ SLOTS ]")
                                     ])
        mock_run.assert_called_once()
        mock_print.assert_called_once_with("Invalid input. Please try again\n\n")

    def test_is_password_valid_true(self):
        test_password: str = "validPassword123!"

        self.assertTrue(is_password_valid(test_password))

    def test_is_password_valid_exactly_8_chars(self):
        test_password: str = "validP1!"

        self.assertTrue(is_password_valid(test_password))

    def test_is_password_valid_too_short(self):
        test_password: str = "validPa"

        self.assertFalse(is_password_valid(test_password))

    def test_is_password_valid_no_uppercase(self):
        test_password: str = "valid_password123!"

        self.assertFalse(is_password_valid(test_password))

    def test_is_password_valid_no_lowercase(self):
        test_password: str = "VALID_PASSWORD123!"

        self.assertFalse(is_password_valid(test_password))

    def test_is_password_valid_only_letters(self):
        test_password: str = "vAlIdPaSsWoRd"

        self.assertFalse(is_password_valid(test_password))

    def test_is_password_valid_no_number(self):
        test_password: str = "validPassword!"

        self.assertFalse(is_password_valid(test_password))

    def test_is_password_only_number(self):
        test_password: str = "12345678"

        self.assertFalse(is_password_valid(test_password))

    def test_is_password_valid_no_special(self):
        test_password: str = "validPassword123"

        self.assertFalse(is_password_valid(test_password))

    def test_is_password_only_special(self):
        test_password: str = "!@#$%^&*("

        self.assertFalse(is_password_valid(test_password))

    def test_is_password_invalid_space_char(self):
        test_password: str = "ValidPassword  123!"

        self.assertFalse(is_password_valid(test_password))

    def test_is_password_invalid_tab_char(self):
        test_password: str = "ValidPassword\t123!"

        self.assertFalse(is_password_valid(test_password))

    def test_is_password_invalid_empty_string(self):
        test_password: str = ""

        self.assertFalse(is_password_valid(test_password))

    @patch(f"{ACCOUNT_MANAGER_CLASS_PATH}.update_password")
    @patch(f"{IOCONSOLE_PATH}.get_string_input", return_value="ValidPassword123!")
    @patch(f"{IOCONSOLE_PATH}.print_colored")
    def test_update_password_valid(self, mock_print, mock_input, mock_update):
        actual: bool = self.casino.update_password()

        mock_print.assert_called_once_with("Your password has been updated!", ANSI_COLORS.GREEN)
        mock_update.assert_called_once()

        self.assertTrue(actual)

    @patch(f"{ACCOUNT_MANAGER_CLASS_PATH}.update_password")
    @patch(f"{IOCONSOLE_PATH}.get_string_input", side_effect=["none","ValidPassword123!"])
    @patch(f"{IOCONSOLE_PATH}.print_error")
    @patch(f"{IOCONSOLE_PATH}.print_colored")
    def test_update_password_fail_then_valid(self, mock_print, mock_print_error, mock_input, mock_update):
        actual: bool = self.casino.update_password()

        mock_print_error.assert_called_once_with("Invalid password. Password must follow the following:\n"
                                                 "- At least 8 characters long\n"
                                                 "- At least one uppercase letter\n"
                                                 "- At least one lowercase letter\n"
                                                 "- At least one number\n"
                                                 "- At least one special character")
        mock_input.assert_has_calls([call("Enter new password: ", return_in_lower=False),
                                    call("Enter new password: ", return_in_lower=False)])
        mock_print.assert_called_once_with("Your password has been updated!", ANSI_COLORS.GREEN)
        mock_update.assert_called_once()

        self.assertTrue(actual)

    @patch(f"{ACCOUNT_MANAGER_CLASS_PATH}.update_password")
    @patch(f"{IOCONSOLE_PATH}.get_string_input", side_effect=["none", "none", "none", "none", "none", "none"])
    @patch(f"{IOCONSOLE_PATH}.print_error")
    def test_update_password_max_fail(self, mock_print_error, mock_input, mock_update):
        actual: bool = self.casino.update_password()

        expected_error: str = "Invalid password. Password must follow the following:\n" \
                              "- At least 8 characters long\n" \
                              "- At least one uppercase letter\n" \
                              "- At least one lowercase letter\n" \
                              "- At least one number\n" \
                              "- At least one special character"

        mock_print_error.assert_has_calls([
            call(expected_error),
            call(expected_error),
            call(expected_error),
            call(expected_error),
            call(expected_error),
            call("Too many invalid attempts. Password was not updated.")])

        mock_input.assert_has_calls([
            call("Enter new password: ", return_in_lower=False),
            call("Enter new password: ", return_in_lower=False),
            call("Enter new password: ", return_in_lower=False),
            call("Enter new password: ", return_in_lower=False),
            call("Enter new password: ", return_in_lower=False)])

        mock_update.assert_not_called()

        self.assertFalse(actual)

    @patch(f"{CASINO_CLASS_PATH}.print_welcome")
    @patch(f"{CASINO_CLASS_PATH}.prompt_manage_or_select")
    @patch(f"{CASINO_CLASS_PATH}.handle_initial_action", return_value=UserAccount("test_usr",
                                                                                  "ValidPass123!",
                                                                                  50.0,
                                                                                  "test@email.com", TEST_QUESTIONS))
    def test_run_valid_account(self, mock_action, mock_prompt, mock_print):
        self.casino.run()

        mock_action.assert_called_once()
        mock_prompt.assert_called_once()
        mock_print.assert_called_once()

    @patch(f"{IOCONSOLE_PATH}.print_colored")
    @patch(f"{IOCONSOLE_PATH}.get_integer_input", return_value=1)
    def test_get_security_question(self, mock_input, mock_print):
        possible_questions: list[str] = ["question zero", "question one", "question two", "question three"]

        expected: str = "question one"
        actual: str = self.casino.get_security_question(possible_questions)
        expected_print_count: int = len(possible_questions) + 1
        print_count: int = mock_print.call_count

        self.assertEqual(expected, actual)
        self.assertEqual(expected_print_count, print_count)

    @patch(f"{IOCONSOLE_PATH}.print_colored")
    @patch(f"{IOCONSOLE_PATH}.print_error")
    @patch("builtins.input", side_effect=['-1', "1"])
    def test_get_security_question_invalid(self, mock_input, mock_print_error, mock_print):
        possible_questions: list[str] = ["question zero", "question one", "question two", "question three"]

        expected: str = "question one"
        actual: str = self.casino.get_security_question(possible_questions)
        expected_print_count: int = len(possible_questions) + 1
        print_count: int = mock_print.call_count

        mock_print_error.assert_called_once_with("-1 is out of range. Please enter a value between 0 and 3.")
        self.assertEqual(expected, actual)
        self.assertEqual(expected_print_count, print_count)

    @patch(f"{IOCONSOLE_PATH}.get_string_input", side_effect=['test_answer', "test_answer"])
    @patch(f"{CASINO_CLASS_PATH}.get_security_question",
           side_effect=["What street did you grow up on?", "What was the name of your first pet?"])
    def test_get_security_questions_and_answers(self, mock_get_questions, mock_input):
        expected: list[str] = ["What street did you grow up on?", "test_answer",
                               "What was the name of your first pet?", "test_answer"]
        actual: list[str] = self.casino.get_security_questions_and_answers()
        expected_mock_get_questions_call_count: int = 2
        actual_mock_get_questions_call_count: int = mock_get_questions.call_count

        self.assertEqual(expected, actual)
        self.assertEqual(expected_mock_get_questions_call_count, actual_mock_get_questions_call_count)

    @patch(f"{IOCONSOLE_PATH}.get_string_input", return_value="test_username")
    def test_prompt_username(self, mock_input):
        expected: str = "test_username"
        actual: str = self.casino.prompt_username()

        mock_input.assert_called_once_with("Create your username or type back", return_in_lower=False)
        self.assertEqual(expected, actual)

    @patch(f"{IOCONSOLE_PATH}.get_string_input", return_value="back")
    def test_prompt_username_back(self, mock_input):
        actual: None = self.casino.prompt_username()

        mock_input.assert_called_once_with("Create your username or type back", return_in_lower=False)
        self.assertIsNone(actual)

    @patch(f"{IOCONSOLE_PATH}.get_string_input", return_value="ValidPass123!")
    def test_prompt_password(self, mock_input):
        expected: str = "ValidPass123!"
        actual: str = self.casino.prompt_password()

        mock_input.assert_called_once_with("Create your password: ", return_in_lower=False)
        self.assertEqual(expected, actual)

    @patch(f"{IOCONSOLE_PATH}.get_string_input",
           side_effect=["invalid_password", "ValidPassword123!"])
    @patch(f"{IOCONSOLE_PATH}.print_error")
    def test_prompt_password_invalid(self, mock_print, mock_inputs):
        expected: str = "ValidPassword123!"
        actual: str = self.casino.prompt_password()

        mock_print.assert_called_once_with("Invalid password. Password must follow the following:\n"
                                           "- At least 8 characters long\n"
                                           "- At least one uppercase letter\n"
                                           "- At least one lowercase letter\n"
                                           "- At least one number\n"
                                           "- At least one special character")

        expected_call_count: int = 2
        actual_call_count: int = mock_inputs.call_count

        self.assertEqual(expected, actual)
        self.assertEqual(expected_call_count, actual_call_count)

    @patch(f"{IOCONSOLE_PATH}.get_string_input", return_value="email@testdomain.com")
    def test_prompt_email_valid(self, mock_input):
        expected: str = "email@testdomain.com"
        actual: str = self.casino.prompt_email()

        mock_input.assert_called_once_with("Enter your email: ", return_in_lower=False)
        self.assertEqual(expected, actual)

    @patch(f"{IOCONSOLE_PATH}.get_string_input", side_effect=["@testdomain.com", "email@testdomain.com"])
    @patch(f"{IOCONSOLE_PATH}.print_error")
    def test_prompt_email_invalid_no_char_before_at(self, mock_print, mock_input):
        expected: str = "email@testdomain.com"
        actual: str = self.casino.prompt_email()

        mock_print.assert_called_once_with("Invalid email.")
        mock_input.assert_has_calls([call("Enter your email: ", return_in_lower=False),
                                     call("Enter your email: ", return_in_lower=False)])
        self.assertEqual(expected, actual)

    @patch(f"{IOCONSOLE_PATH}.get_string_input", side_effect=["emailtestdomain.com", "email@testdomain.com"])
    @patch(f"{IOCONSOLE_PATH}.print_error")
    def test_prompt_email_invalid_no_at(self, mock_print, mock_input):
        expected: str = "email@testdomain.com"
        actual: str = self.casino.prompt_email()

        mock_print.assert_called_once_with("Invalid email.")
        mock_input.assert_has_calls([call("Enter your email: ", return_in_lower=False),
                                     call("Enter your email: ", return_in_lower=False)])
        self.assertEqual(expected, actual)

    @patch(f"{IOCONSOLE_PATH}.get_string_input", side_effect=["email@testdomaincom", "email@testdomain.com"])
    @patch(f"{IOCONSOLE_PATH}.print_error")
    def test_prompt_email_invalid_no_dot(self, mock_print, mock_input):
        expected: str = "email@testdomain.com"
        actual: str = self.casino.prompt_email()

        mock_print.assert_called_once_with("Invalid email.")
        mock_input.assert_has_calls([call("Enter your email: ", return_in_lower=False),
                                     call("Enter your email: ", return_in_lower=False)])
        self.assertEqual(expected, actual)

    @patch(f"{IOCONSOLE_PATH}.get_string_input", side_effect=["email@testdomain.", "email@testdomain.com"])
    @patch(f"{IOCONSOLE_PATH}.print_error")
    def test_prompt_email_invalid_no_char_after_dot(self, mock_print, mock_input):
        expected: str = "email@testdomain.com"
        actual: str = self.casino.prompt_email()

        mock_print.assert_called_once_with("Invalid email.")
        mock_input.assert_has_calls([call("Enter your email: ", return_in_lower=False),
                                     call("Enter your email: ", return_in_lower=False)])
        self.assertEqual(expected, actual)

    @patch(f"{IOCONSOLE_PATH}.get_string_input", side_effect=["email@testdomain.c", "email@testdomain.com"])
    @patch(f"{IOCONSOLE_PATH}.print_error")
    def test_prompt_email_invalid_one_char_after_dot(self, mock_print, mock_input):
        expected: str = "email@testdomain.com"
        actual: str = self.casino.prompt_email()

        mock_print.assert_called_once_with("Invalid email.")
        mock_input.assert_has_calls([call("Enter your email: ", return_in_lower=False),
                                     call("Enter your email: ", return_in_lower=False)])
        self.assertEqual(expected, actual)

    @patch(f"{IOCONSOLE_PATH}.get_string_input", side_effect=["email@testdomain.c",
                                                              "emailtestdomain.com",
                                                              "email@testdomain.com"])
    @patch(f"{IOCONSOLE_PATH}.print_error")
    def test_prompt_email_multiple_invalid(self, mock_print, mock_input):
        expected: str = "email@testdomain.com"
        actual: str = self.casino.prompt_email()

        mock_print.assert_has_calls([call("Invalid email."), call("Invalid email.")])
        mock_input.assert_has_calls([call("Enter your email: ", return_in_lower=False),
                                     call("Enter your email: ", return_in_lower=False),
                                     call("Enter your email: ", return_in_lower=False)])
        self.assertEqual(expected, actual)

    def test_is_token_valid_true(self):
        token: uuid.UUID = uuid.uuid4()
        self.account.reset_token = token
        self.account.reset_token_expiration = datetime.datetime.now(datetime.UTC) + datetime.timedelta(minutes=15)

        actual: bool = self.casino.is_token_valid(str(token))
        self.assertTrue(actual)

    def test_is_token_valid_incorrect_token(self):
        token: uuid.UUID = uuid.uuid4()
        self.account.reset_token = uuid.uuid4()
        self.account.reset_token_expiration = datetime.datetime.now(datetime.UTC) + datetime.timedelta(minutes=15)

        actual: bool = self.casino.is_token_valid(str(token))
        self.assertFalse(actual)

    def test_is_token_valid_not_uuid(self):
        token: str = "invalid token"
        self.account.reset_token = uuid.uuid4()
        self.account.reset_token_expiration = datetime.datetime.now(datetime.UTC) + datetime.timedelta(minutes=15)

        actual: bool = self.casino.is_token_valid(token)
        self.assertFalse(actual)

    def test_is_token_valid_expired(self):
        token: uuid.UUID = uuid.uuid4()
        self.account.reset_token = token
        self.account.reset_token_expiration = datetime.datetime.now(datetime.UTC) - datetime.timedelta(minutes=1)

        actual: bool = self.casino.is_token_valid(str(token))
        self.assertFalse(actual)

    @patch(f"{IOCONSOLE_PATH}.get_string_input", return_value=str(uuid.uuid4()))
    @patch(f"{CASINO_CLASS_PATH}.is_token_valid", return_value=True)
    @patch(f"{CASINO_CLASS_PATH}.update_password", return_value=True)
    @patch(f"{ACCOUNT_MANAGER_CLASS_PATH}.invalidate_reset_token")
    @patch(f"{IOCONSOLE_PATH}.print_error")
    def test_validate_and_reset_valid(self, mock_print, mock_reset, mock_is_token_valid, mock_invalidate, mock_input):
        actual: bool = self.casino.validate_and_reset()

        mock_print.assert_not_called()
        mock_invalidate.assert_called_once()
        mock_reset.assert_called_once()
        mock_is_token_valid.assert_called_once()
        mock_input.is_called_once_with("Please enter your reset token sent to your email")
        self.assertTrue(actual)

    @patch(f"{IOCONSOLE_PATH}.print_error")
    @patch(f"{IOCONSOLE_PATH}.get_string_input", side_effect=["not-a-uuid"] * 5)
    @patch("Application.Casino.Casino.Casino.reset_password")
    def test_validate_and_reset_non_uuid_token(self, mock_reset, mock_input, mock_error):
        self.account.reset_token = uuid.uuid4()
        self.account.reset_token_expiration = datetime.datetime.now(datetime.UTC) + datetime.timedelta(minutes=15)

        actual: bool = self.casino.validate_and_reset()

        mock_reset.assert_not_called()
        self.assertEqual(mock_error.call_count, 6)
        self.assertFalse(actual)

    @patch(f"{IOCONSOLE_PATH}.print_error")
    @patch(f"{IOCONSOLE_PATH}.get_string_input", side_effect=[str(uuid.uuid4())] * 5)
    @patch("Application.Casino.Casino.Casino.reset_password")
    def test_validate_and_reset_wrong_token(self, mock_reset, mock_input, mock_error):
        self.account.reset_token = uuid.uuid4()
        self.account.reset_token_expiration = datetime.datetime.now(datetime.UTC) + datetime.timedelta(minutes=15)

        actual: bool = self.casino.validate_and_reset()

        mock_reset.assert_not_called()
        self.assertEqual(mock_error.call_count, 6)
        self.assertFalse(actual)

    @patch(f"{IOCONSOLE_PATH}.print_error")
    @patch(f"{IOCONSOLE_PATH}.get_string_input")
    @patch("Application.Casino.Casino.Casino.reset_password")
    def test_validate_and_reset_expired_token(self, mock_reset, mock_input, mock_error):
        token = uuid.uuid4()
        self.account.reset_token = token
        self.account.reset_token_expiration = datetime.datetime.now(datetime.UTC) - datetime.timedelta(minutes=1)
        mock_input.side_effect = [str(token)] * 5

        actual: bool = self.casino.validate_and_reset()

        mock_reset.assert_not_called()
        self.assertEqual(mock_error.call_count, 6)
        self.assertFalse(actual)

    @patch(f"{IOCONSOLE_PATH}.get_string_input", return_value="test@email.com")
    @patch(f"{ACCOUNT_MANAGER_CLASS_PATH}.get_account_by_email", return_value=True)
    @patch(f"{IOCONSOLE_PATH}.print_error")
    def test_prompt_and_check_email_valid(self, mock_print, mock_get_account, mock_input):
        actual: bool = self.casino.prompt_and_check_email()

        self.assertTrue(actual)
        mock_print.assert_not_called()
        mock_get_account.assert_called_once_with("test@email.com")
        mock_input.assert_called_once_with("Please enter the email associated with your account: ")

    @patch(f"{IOCONSOLE_PATH}.get_string_input", side_effect=["incorrect_email", "test@email.com"])
    @patch(f"{ACCOUNT_MANAGER_CLASS_PATH}.get_account_by_email",
           side_effect=[None,UserAccount("test_username", "ValidPassword123!",50.0,
                                         "test@email.com", TEST_QUESTIONS)])
    @patch(f"{IOCONSOLE_PATH}.print_error")
    def test_prompt_and_check_email_invalid_then_valid(self, mock_print, mock_get_account, mock_input):
        actual: bool = self.casino.prompt_and_check_email()

        self.assertTrue(actual)
        mock_print.assert_called_once_with("Invalid email. Please try again.")
        mock_get_account.assert_has_calls([call("incorrect_email"), call("test@email.com")])
        mock_input.assert_has_calls([call("Please enter the email associated with your account: "),
                                     call("Please enter the email associated with your account: ")])

    @patch(f"{IOCONSOLE_PATH}.get_string_input", side_effect=["email", "email", "email", "email", "email"])
    @patch(f"{IOCONSOLE_PATH}.print_error")
    def test_prompt_and_check_email_max_invalid(self, mock_print, mock_input):
        actual: bool = self.casino.prompt_and_check_email()

        self.assertFalse(actual)
        mock_print.assert_has_calls([call("Invalid email. Please try again."),
                                     call("Invalid email. Please try again."),
                                     call("Invalid email. Please try again."),
                                     call("Invalid email. Please try again."),
                                     call("Invalid email. Please try again."),
                                     call("Too many attempts. Try again later.")])
        mock_input.assert_has_calls([call("Please enter the email associated with your account: "),
                                     call("Please enter the email associated with your account: "),
                                     call("Please enter the email associated with your account: "),
                                     call("Please enter the email associated with your account: "),
                                     call("Please enter the email associated with your account: ")])

    @patch(f"{IOCONSOLE_PATH}.get_string_input", return_value="Test Answer")
    def test_prompt_for_security_answer_valid(self, mock_input):
        actual: bool = self.casino.prompt_for_security_answer("Test Question", "Test Answer")

        self.assertTrue(actual)
        mock_input.assert_called_once_with("Test Question")

    @patch(f"{IOCONSOLE_PATH}.get_string_input", return_value="  Test Answer  ")
    def test_prompt_for_security_answer_valid_with_strip(self, mock_input):
        actual: bool = self.casino.prompt_for_security_answer("Test Question", " Test Answer")

        self.assertTrue(actual)
        mock_input.assert_called_once_with("Test Question")

    @patch(f"{IOCONSOLE_PATH}.get_string_input", side_effect=["Wrong Answer", "Test Answer"])
    @patch(f"{IOCONSOLE_PATH}.print_error")
    def test_prompt_for_security_answer_invalid_then_valid(self, mock_print, mock_input):
        actual: bool = self.casino.prompt_for_security_answer("Test Question", "Test Answer")

        self.assertTrue(actual)
        mock_input.assert_has_calls([call("Test Question"), call("Test Question")])
        mock_print.assert_called_once_with("Incorrect answer. Please try again.")

    @patch(f"{IOCONSOLE_PATH}.get_string_input", side_effect=["Answer", "Answer", "Answer", "Answer", "Answer"])
    @patch(f"{IOCONSOLE_PATH}.print_error")
    def test_prompt_for_security_answer_max_attempts(self, mock_print, mock_input):
        expected_input_call_count: int = 5
        actual: bool = self.casino.prompt_for_security_answer("Test Question", "Test Answer")
        actual_input_call_count: int = mock_input.call_count

        self.assertEqual(actual_input_call_count, expected_input_call_count)
        self.assertFalse(actual)
        mock_print.assert_has_calls([call("Incorrect answer. Please try again."),
                                     call("Incorrect answer. Please try again."),
                                     call("Incorrect answer. Please try again."),
                                     call("Incorrect answer. Please try again."),
                                     call("Incorrect answer. Please try again."),
                                     call("Too many attempts. Try again later.")])

    @patch(f"{CASINO_CLASS_PATH}.prompt_for_security_answer", side_effect=[True, True])
    def test_get_security_answers_true(self, mock_prompt):
        actual: bool = self.casino.get_security_answers()

        mock_prompt.assert_has_calls([call(self.casino.account.security_question_one,
                                           self.casino.account.security_answer_one),
                                      call(self.casino.account.security_question_two,
                                           self.casino.account.security_answer_two)])
        self.assertTrue(actual)

    @patch(f"{CASINO_CLASS_PATH}.prompt_for_security_answer", return_value=False)
    def test_get_security_answers_failed_first_question(self, mock_prompt):
        actual: bool = self.casino.get_security_answers()

        mock_prompt.assert_called_once_with(self.casino.account.security_question_one,
                                           self.casino.account.security_answer_one)
        self.assertFalse(actual)

    @patch(f"{CASINO_CLASS_PATH}.prompt_for_security_answer", side_effect=[True, False])
    def test_get_security_answers_failed_second_question(self, mock_prompt):
        actual: bool = self.casino.get_security_answers()

        mock_prompt.assert_has_calls([call(self.casino.account.security_question_one,
                                           self.casino.account.security_answer_one),
                                      call(self.casino.account.security_question_two,
                                           self.casino.account.security_answer_two)])
        self.assertFalse(actual)

    @patch(f"{CASINO_CLASS_PATH}.prompt_and_check_email", return_value=True)
    @patch(f"{CASINO_CLASS_PATH}.get_security_answers", return_value=True)
    @patch(f"{CASINO_CLASS_PATH}.validate_and_reset")
    @patch(f"{ACCOUNT_MANAGER_CLASS_PATH}.email_recovery_token")
    def test_reset_from_login_true(self, mock_email, mock_validate, mock_get_answers, mock_prompt_email):
        actual: bool = self.casino.reset_from_login()

        mock_prompt_email.assert_called_once()
        mock_get_answers.assert_called_once()
        mock_validate.assert_called_once()
        mock_email.assert_called_once()
        self.assertTrue(actual)

    @patch(f"{CASINO_CLASS_PATH}.prompt_and_check_email", return_value=False)
    def test_reset_from_login_fail_prompt_email(self, mock_prompt_email):
        actual: bool = self.casino.reset_from_login()

        mock_prompt_email.assert_called_once()
        self.assertFalse(actual)

    @patch(f"{CASINO_CLASS_PATH}.prompt_and_check_email", return_value=True)
    @patch(f"{CASINO_CLASS_PATH}.get_security_answers", return_value=False)
    def test_reset_from_login_fail_security_questions(self, mock_get_answers, mock_prompt_email):
        actual: bool = self.casino.reset_from_login()

        mock_prompt_email.assert_called_once()
        mock_get_answers.assert_called_once()
        self.assertFalse(actual)

    @patch(f"{CASINO_CLASS_PATH}.prompt_and_check_email", return_value=True)
    @patch(f"{CASINO_CLASS_PATH}.get_security_answers", return_value=True)
    @patch(f"{CASINO_CLASS_PATH}.validate_and_reset", return_value=False)
    @patch(f"{ACCOUNT_MANAGER_CLASS_PATH}.email_recovery_token")
    def test_reset_from_login_fail_validate(self, mock_email, mock_validate, mock_get_answers, mock_prompt_email):
        actual: bool = self.casino.reset_from_login()

        mock_prompt_email.assert_called_once()
        mock_get_answers.assert_called_once()
        mock_validate.assert_called_once()
        mock_email.assert_called_once()
        self.assertFalse(actual)