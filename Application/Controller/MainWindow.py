import tkinter as tk
from tkinter import ttk

from Application.Controller.AccountController import AccountController
from Application.Controller.Games.GameController import GameController
from Application.Utils.LoggingController import setup_logging
from Application.Model.Accounts.AccountManager import AccountManager
from Application.View.BaseFrame import BaseFrame
from Application.View.EntryFrame import EntryFrame
from Application.View.GameSelectionFrame import GameSelectionFrame
from Application.View.PasswordResetFrame import PasswordResetFrame

setup_logging()


class MainWindow(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Python Casino!")
        self.geometry("800x800")
        account_manager: AccountManager = AccountManager()
        self.account_controller: AccountController = AccountController(account_manager)
        self.game_controller: GameController = GameController(self.account_controller)

        self.container: ttk.Frame = ttk.Frame(self)
        self.container.pack(fill="both", expand=True)

        self.menu_bar: tk.Menu = tk.Menu()
        self.empty_menu: tk.Menu = tk.Menu()
        self.create_menu()

        # self.render_frame(EntryFrame, show_menu=False)
        self.render_frame(GameSelectionFrame)

    def render_frame(self, new_frame: type[BaseFrame], show_menu: bool = True, **kwargs) -> None:
        """
        Destroys previous frame and renders new frame.
        :param new_frame: A new Frame object.
        :param show_menu: A boolean representing whether to show the menu.
        :return: None
        """
        for frame in self.container.winfo_children():
            frame.destroy()

        self.config(menu=self.menu_bar if show_menu else self.empty_menu)

        frame: ttk.Frame = new_frame(self.container, self, **kwargs)
        frame.pack(fill="both", expand=True)

    def create_menu(self) -> None:
        """
        Creates the top menu bar for easier application navigation.
        :return: None
        """
        # Account Menu
        account_menu: tk.Menu = tk.Menu(self.menu_bar, tearoff=False)
        self.menu_bar.add_cascade(label="Account", menu=account_menu)
        account_menu.add_command(label="Add Funds", command="")
        account_menu.add_command(label="Manage Security Questions", command="")
        account_menu.add_command(label="Reset Password", command=self.transition_to_password_reset)

        # Game Menu
        game_menu: tk.Menu = tk.Menu(self.menu_bar, tearoff=False)
        self.menu_bar.add_cascade(label="Games", menu=game_menu)
        game_menu.add_command(label="Coin Flip", command=self.transition_to_coinflip)
        game_menu.add_command(label="Number Guess", command=self.transition_to_ng)
        game_menu.add_command(label="RPS", command=self.transition_to_rps)
        game_menu.add_command(label="Slots", command=self.transition_to_slots)
        game_menu.add_command(label="TicTacToe", command=self.transition_to_ttt)
        game_menu.add_command(label="Trivia", command=self.transition_to_trivia)

        # Home menu
        home_menu: tk.Menu = tk.Menu(self.menu_bar, tearoff=False)
        self.menu_bar.add_cascade(label="Home", menu=home_menu)
        home_menu.add_command(label="Main Menu", command=self.transition_to_main_menu)
        home_menu.add_command(label="Quit", command=self.quit)

        self.configure(menu=self.menu_bar)

    def transition_to_password_reset(self):
        """
        Transitions to PasswordResetFrame
        :return: None
        """
        self.render_frame(PasswordResetFrame)

    def transition_to_main_menu(self) -> None:
        """
        Transitions to MainMenu
        :return: None
        """

        from Application.View.MainMenuFrame import MainMenuFrame
        self.render_frame(MainMenuFrame)

    def transition_to_coinflip(self) -> None:
        """
        Transitions to CoinFlipFrame
        :return: None
        """
        from Application.View.GameViews.CoinFlipFrame import CoinFlipFrame
        self.render_frame(CoinFlipFrame)

    def transition_to_ng(self) -> None:
        """
        Transitions to NumberGuessFrame
        :return: None
        """
        from Application.View.GameViews.NumberGuessFrame import NumberGuessFrame
        self.render_frame(NumberGuessFrame)

    def transition_to_rps(self) -> None:
        """
        Transitions to RpsFrame
        :return: None
        """
        from Application.View.GameViews.RpsFrame import RpsFrame
        self.render_frame(RpsFrame)

    def transition_to_slots(self) -> None:
        """
        Transitions to SlotFrame
        :return: None
        """
        from Application.View.GameViews.SlotsFrame import SlotsFrame
        self.render_frame(SlotsFrame)

    def transition_to_ttt(self) -> None:
        """
        Transitions to TicTacToeFrame
        :return: None
        """
        from Application.View.GameViews.TicTacToeFrame import TicTacToeFrame
        self.render_frame(TicTacToeFrame)

    def transition_to_trivia(self) -> None:
        """
        Transitions to TriviaFrame
        :return: None
        """
        from Application.View.GameViews.TriviaGameFrame import TriviaGameFrame
        self.render_frame(TriviaGameFrame)


if __name__ == "__main__":
    app = MainWindow()
    app.mainloop()
