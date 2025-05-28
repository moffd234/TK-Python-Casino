from unittest.mock import patch
from Application.Casino.Games.TicTacToe.TicTacToe import TicTacToe, main
from Application.Utils.ANSI_COLORS import ANSI_COLORS
from Tests.BaseTest import BaseTest, IOCONSOLE_PATH, TICTACTOE_CLASS_PATH, GAME_CLASS_PATH, TICTACTOE_FILE_PATH


class TestTicTacToe(BaseTest):

    def setUp(self):
        super().setUp()
        self.game = TicTacToe(self.manager.get_account("Username", "Password"), self.manager)

    def assert_handle_turn(self, expected_turn, expected_board):
        self.game.handle_turn()
        actual_turn: str = self.game.turn
        actual_board: list[list[str]] = self.game.game_board

        self.assertEqual(expected_turn, actual_turn)
        self.assertEqual(expected_board, actual_board)

    def run_and_assert(self, mock_play, mock_print, mock_print_board, mock_print_welcome):
        self.game.run()
        self.game.game_board = [["x", "o", "x"], ["x", "o", "o"], ["x", " ", " "]]
        mock_print_board.assert_called_once()
        mock_play.assert_called_once()
        mock_print_welcome.assert_called_once()

        if mock_play.return_value != "tie":
            mock_print.assert_any_call(f"Winner is {mock_play.return_value}", ANSI_COLORS.GREEN)

        else:
            mock_print.assert_any_call("Game Over. It is a tie")

    @patch("builtins.print")
    def test_print_welcome_message(self, mock_print):
        expected: str = r"""[36m
         __          __  _                            _______      _______ _          _______             _______         
         \ \        / / | |                          |__   __|    |__   __(_)        |__   __|           |__   __|        
          \ \  /\  / /__| | ___ ___  _ __ ___   ___     | | ___      | |   _  ___ ______| | __ _  ___ ______| | ___   ___ 
           \ \/  \/ / _ \ |/ __/ _ \| '_ ` _ \ / _ \    | |/ _ \     | |  | |/ __|______| |/ _` |/ __|______| |/ _ \ / _ \
            \  /\  /  __/ | (_| (_) | | | | | |  __/    | | (_) |    | |  | | (__       | | (_| | (__       | | (_) |  __/
             \/  \/ \___|_|\___\___/|_| |_| |_|\___|    |_|\___/     |_|  |_|\___|      |_|\__,_|\___|      |_|\___/ \___|
                                                                                                                          
            
            Rules:
                This is a non-gambling game so you will not win or lose money.
                Two players take turns placing their symbol on the board.
                The first player to place three of their symbols in a horizontal, vertical, or diagonal row wins.                                                                                                    
        """

        self.game.print_welcome_message()
        mock_print.assert_called_once_with(expected)

    def test_check_for_winner_horizontal(self):
        self.game.game_board = \
            [["x", "x", "x"],
             [" ", " ", " "],
             [" ", " ", " "]]

        expected: str = "x"
        actual: str = self.game.check_for_winner()
        self.assertEqual(expected, actual)

    def test_check_for_winner_horizontal_middle(self):
        self.game.game_board =\
            [["o", "x", "x"],
             ["o", "o", "o"],
             [" ", " ", " "]]

        expected: str = "o"
        actual: str = self.game.check_for_winner()
        self.assertEqual(expected, actual)

    def test_check_for_winner_horizontal_last(self):
        self.game.game_board =\
            [["o", "x", "x"],
             ["o", "o", "o"],
             ["x", "x", "x"]]

        expected: str = "o"
        actual: str = self.game.check_for_winner()
        self.assertEqual(expected, actual)

    def test_check_for_winner_vertical_first(self):
        self.game.game_board = \
            [["o", "o", "x"],
             ["o", "x", "o"],
             ["o", "x", "x"]]

        expected: str = "o"
        actual: str = self.game.check_for_winner()
        self.assertEqual(expected, actual)

    def test_check_for_winner_vertical_second(self):
        self.game.game_board = \
            [["o", "x", "x"],
             ["x", "x", "o"],
             ["o", "x", "x"]]

        expected: str = "x"
        actual: str = self.game.check_for_winner()
        self.assertEqual(expected, actual)

    def test_check_for_winner_vertical_last(self):
        self.game.game_board = \
            [["o", "x", "x"],
             ["x", "o", "x"],
             ["o", "x", "x"]]

        expected: str = "x"
        actual: str = self.game.check_for_winner()
        self.assertEqual(expected, actual)

    def test_check_for_winner_diagonal_bottom_to_top(self):
        self.game.game_board = \
            [["o", "x", "x"],
             ["o", "x", "o"],
             ["x", "o", "x"]]

        expected: str = "x"
        actual: str = self.game.check_for_winner()
        self.assertEqual(expected, actual)

    def test_check_for_winner_diagonal_top_to_bottom(self):
        self.game.game_board = \
            [["x", "o", "x"],
             ["o", "x", "o"],
             ["o", "x", "x"]]

        expected: str = "x"
        actual: str = self.game.check_for_winner()
        self.assertEqual(expected, actual)

    def test_check_for_winner_none(self):
        self.game.game_board = \
            [["x", "o", "x"],
             ["o", "x", "o"],
             ["o", "x", "o"]]

        expected: None = None
        actual: None = self.game.check_for_winner()
        self.assertEqual(expected, actual)

    def test_is_cell_empty_false(self):
        self.game.game_board = \
            [["x", "x", "x"],
             [" ", " ", " "],
             [" ", " ", " "]]

        actual: bool = self.game.is_cell_empty(0, 0)
        self.assertFalse(actual)

    def test_is_cell_empty_true(self):
        self.game.game_board = \
            [["x", "x", "x"],
             [" ", " ", " "],
             [" ", " ", " "]]

        actual: bool = self.game.is_cell_empty(1, 0)
        self.assertTrue(actual)

    @patch(f"{IOCONSOLE_PATH}.get_integer_input", return_value=1)
    def test_get_row_first_try(self, mock_input):
        expected: int = 1
        actual: int = self.game.get_row()
        self.assertEqual(expected, actual)

    @patch(f"{IOCONSOLE_PATH}.get_integer_input", return_value=1)
    def test_get_col_first_try(self, mock_input):

        expected: int = 1
        actual: int = self.game.get_col()
        self.assertEqual(expected, actual)

    @patch(f"{IOCONSOLE_PATH}.print_colored")
    def test_print_board_empty(self, mock_print):
        expected: str = ("  |   |  "
                        "\n---------\n"
                        "  |   |  "
                        "\n---------\n"
                        "  |   |  ")
        self.game.print_board()
        mock_print.assert_called_once_with(expected)

    @patch(f"{IOCONSOLE_PATH}.print_colored")
    def test_print_board_full(self, mock_print):
        self.game.game_board = [["x", "o", "x"],["o", "x", "o"],["x", "o", "x"]]
        expected: str = ("x | o | x"
                         "\n---------\n"
                         "o | x | o"
                         "\n---------\n"
                         "x | o | x")
        self.game.print_board()
        mock_print.assert_called_once_with(expected)

    @patch(f"{TICTACTOE_CLASS_PATH}.get_row", return_value=1)
    @patch(f"{TICTACTOE_CLASS_PATH}.get_col", return_value=1)
    def test_handle_turn_valid_x_turn(self, mock_col, mock_row):
        self.game.turn = 'x'
        expected_turn: str = 'o'
        expected_board: list[list[str]] = [["x", " ", " "],[" ", " ", " "],[" ", " ", " "]]

        self.assert_handle_turn(expected_turn, expected_board)

    @patch(f"{TICTACTOE_CLASS_PATH}.get_row", return_value=2)
    @patch(f"{TICTACTOE_CLASS_PATH}.get_col", return_value=1)
    def test_handle_turn_valid_o_turn(self, mock_col, mock_row):
        self.game.turn = 'o'
        expected_turn: str = 'x'
        expected_board: list[list[str]] = [[" ", " ", " "], ["o", " ", " "], [" ", " ", " "]]

        self.assert_handle_turn(expected_turn, expected_board)

    @patch(f"{TICTACTOE_CLASS_PATH}.get_row", side_effect=[1, 2])
    @patch(f"{TICTACTOE_CLASS_PATH}.get_col", side_effect=[1, 1])
    @patch(f"{IOCONSOLE_PATH}.print_error")
    def test_handle_turn_invalid_o_turn(self, mock_print, mock_col, mock_row):
        self.game.turn = 'o'
        self.game.game_board = [["x", " ", " "], [" ", " ", " "], [" ", " ", " "]]

        with patch.object(self.game.console, "print_error") as mock_print:
            expected_turn: str = 'x'
            expected_board: list[list[str]] = [["x", " ", " "], ["o", " ", " "], [" ", " ", " "]]

            self.assert_handle_turn(expected_turn, expected_board)
            mock_print.assert_called_once_with("Cell already occupied")

    @patch(f"{TICTACTOE_CLASS_PATH}.get_row", side_effect=[1, 2])
    @patch(f"{TICTACTOE_CLASS_PATH}.get_col", side_effect=[1, 1])
    def test_handle_turn_invalid_x_turn(self, mock_col, mock_row):
        self.game.turn = 'x'
        self.game.game_board = [["o", " ", " "], [" ", " ", " "], [" ", " ", " "]]

        with patch.object(self.game.console, "print_error") as mock_print:
            expected_turn: str = 'o'
            expected_board: list[list[str]] = [["o", " ", " "], ["x", " ", " "], [" ", " ", " "]]

            self.assert_handle_turn(expected_turn, expected_board)
            mock_print.assert_called_once_with("Cell already occupied")

    def test_is_board_full_true(self):
        self.game.game_board = [
            ["x", "o", "x"],
            ["o", "x", "o"],
            ["o", "x", "o"]
        ]
        self.assertTrue(self.game.is_board_full())

    def test_is_board_full_false(self):
        self.game.game_board = [[" " for _ in range(3)]]
        self.assertFalse(self.game.is_board_full())

    @patch(f"{TICTACTOE_CLASS_PATH}.print_welcome_message")
    @patch(f"{GAME_CLASS_PATH}.get_continue_input", side_effect=[True, False])
    @patch(f"{TICTACTOE_CLASS_PATH}.play_game", return_value="x")
    @patch(f"{TICTACTOE_CLASS_PATH}.print_board")
    @patch(f"{IOCONSOLE_PATH}.print_colored")
    def test_run_once_x_win(self, mock_print, mock_print_board, mock_play, mock_continue_input, mock_print_welcome):
        self.run_and_assert(mock_play, mock_print, mock_print_board, mock_print_welcome)

        expected_call_count = 2
        self.assertEqual(expected_call_count, mock_continue_input.call_count)

    @patch(f"{TICTACTOE_CLASS_PATH}.print_welcome_message")
    @patch(f"{GAME_CLASS_PATH}.get_continue_input", side_effect=[True, False])
    @patch(f"{TICTACTOE_CLASS_PATH}.play_game", return_value="o")
    @patch(f"{TICTACTOE_CLASS_PATH}.print_board")
    @patch(f"{IOCONSOLE_PATH}.print_colored")
    def test_run_once_o_win(self, mock_print, mock_print_board, mock_play, mock_continue_input, mock_print_welcome):
        self.run_and_assert(mock_play, mock_print, mock_print_board, mock_print_welcome)

        expected_call_count = 2
        self.assertEqual(expected_call_count, mock_continue_input.call_count)

    @patch(f"{TICTACTOE_CLASS_PATH}.print_welcome_message")
    @patch(f"{GAME_CLASS_PATH}.get_continue_input", side_effect=[True, False])
    @patch(f"{TICTACTOE_CLASS_PATH}.play_game", return_value="tie")
    @patch(f"{TICTACTOE_CLASS_PATH}.print_board")
    @patch(f"{IOCONSOLE_PATH}.print_colored")
    def test_run_once_tie(self, mock_print, mock_print_board, mock_play, mock_continue_input, mock_print_welcome):
        self.run_and_assert(mock_play, mock_print, mock_print_board, mock_print_welcome)

        expected_call_count = 2
        self.assertEqual(expected_call_count, mock_continue_input.call_count)

    @patch(f"{TICTACTOE_CLASS_PATH}.print_welcome_message")
    @patch(f"{GAME_CLASS_PATH}.get_continue_input", side_effect=[True, True, False])
    @patch(f"{TICTACTOE_CLASS_PATH}.play_game", side_effect=["o", "tie"])
    @patch(f"{TICTACTOE_CLASS_PATH}.print_board")
    @patch(f"{IOCONSOLE_PATH}.print_colored")
    def test_run_twice(self, mock_print, mock_print_board, mock_play, mock_continue_input, mock_print_welcome):
        self.game.run()

        expected_call_count = 2
        self.assertEqual(expected_call_count, mock_print_board.call_count)
        self.assertEqual(expected_call_count, mock_play.call_count)
        self.assertEqual(expected_call_count + 1, mock_continue_input.call_count)
        self.assertEqual(expected_call_count - 1, mock_print_welcome.call_count)

        mock_print.assert_any_call(f"Winner is o", ANSI_COLORS.GREEN)
        mock_print.assert_any_call("Game Over. It is a tie")

    @patch(f"{TICTACTOE_FILE_PATH}.os.remove")
    @patch(f"{TICTACTOE_FILE_PATH}.os.path.exists", return_value=True)
    @patch(f"{TICTACTOE_CLASS_PATH}.run")
    def test_main(self, mock_run, mock_exists, mock_remove):
        main()

        mock_run.assert_called_once()
        mock_exists.assert_called_once_with("casino.db")
        mock_remove.assert_called_once_with("casino.db")