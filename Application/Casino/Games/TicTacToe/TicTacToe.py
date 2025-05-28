import os
from Application.Casino.Accounts.AccountManager import AccountManager
from Application.Casino.Accounts.UserAccount import UserAccount
from Application.Casino.Games.Game import Game
from Application.Utils.ANSI_COLORS import ANSI_COLORS


class TicTacToe(Game):
    def __init__(self, player: UserAccount, manager: AccountManager):
        super().__init__(player, manager)
        self.console.color = ANSI_COLORS.CYAN.value
        self.game_board: list[list[str]] = [[" " for _ in range(3)] for _ in range(3)]
        self.turn = "x"

    def print_welcome_message(self) -> None:
        self.console.print_colored(r"""
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
                                   )

    def run(self):
        self.print_welcome_message()

        while self.get_continue_input():
            winner: str | None = self.play_game()
            if winner == "tie":
                self.console.print_colored("Game Over. It is a tie")
            else:
                self.console.print_success(f"Winner is {winner}")
            self.print_board()

    def print_board(self) -> None:
        board_lines = []
        for row in self.game_board:
            board_lines.append(" | ".join(row))
        board_display = "\n---------\n".join(board_lines)
        self.console.print_colored(board_display)

    def is_cell_empty(self, row: int, col: int) -> bool:
        return self.game_board[row][col] == " "

    def get_row(self) -> int:
        return self.console.get_integer_input("Enter row number (1-3)", range_vals=[1, 3])

    def get_col(self) -> int:
        col = self.console.get_integer_input("Enter column number (1-3)", range_vals=[1, 3])

        return col

    def handle_turn(self) -> None:
        row = self.get_row()
        col = self.get_col()

        while not self.is_cell_empty(row - 1, col - 1):
            self.console.print_error("Cell already occupied")
            row = self.get_row()
            col = self.get_col()

        self.game_board[row - 1][col - 1] = self.turn
        self.turn = "o" if self.turn == "x" else "x"

    def check_for_winner(self) -> str | None:
        for row in range(3):
            # Horizontal
            if self.game_board[row][0] == self.game_board[row][1] == self.game_board[row][2] != " ":
                return self.game_board[row][0]

            # Vertical
            if self.game_board[0][row] == self.game_board[1][row] == self.game_board[2][row] != " ":
                return self.game_board[0][row]

        # Diagonal
        if self.game_board[0][0] == self.game_board[1][1] == self.game_board[2][2] != " ":
            return self.game_board[0][0]

        # Diagonal
        if self.game_board[0][2] == self.game_board[1][1] == self.game_board[2][0] != " ":
            return self.game_board[0][2]

        return None

    def play_game(self) -> str | None:
        winner: str | None = None

        while winner is None:
            self.print_board()
            self.handle_turn()
            winner = self.check_for_winner()

            if winner:
                return winner
            elif self.is_board_full():
                return "tie"

        return None

    def is_board_full(self) -> bool:

        for row in range(3):
            for col in range(3):
                if self.game_board[row][col] == " ":
                    return False

        return True


def main():
    account_manager: AccountManager = AccountManager()
    account: UserAccount = UserAccount("Tester", "ValidPassword123!", 1000, "test@email.com",
                                       ["Who is your favorite sports team?", "Test Answer",
                                        "What street did you grow up on?", "Test Street"])
    game: TicTacToe = TicTacToe(account, account_manager)
    game.run()

    if os.path.exists("casino.db"):
        os.remove("casino.db")


if __name__ == "__main__":
    main()
