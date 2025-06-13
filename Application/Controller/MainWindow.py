import tkinter as tk
from tkinter import ttk

from Application.Controller.AccountController import AccountController
from Application.Utils.LoggingController import setup_logging
from Application.Model.Accounts.AccountManager import AccountManager
from Application.View.BaseFrame import BaseFrame
from Application.View.EntryFrame import EntryFrame
from Application.View.PasswordResetFrame import PasswordResetFrame

setup_logging()


class MainWindow(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Python Casino!")
        self.geometry("800x800")
        account_manager: AccountManager = AccountManager()
        self.account_controller: AccountController = AccountController(account_manager)

        self.container: ttk.Frame = ttk.Frame(self)
        self.container.pack(fill="both", expand=True)

        self.menu_bar: tk.Menu = tk.Menu()
        self.empty_menu: tk.Menu = tk.Menu()
        self.create_menu()

        self.render_frame(EntryFrame, )  # show_menu=False)

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
        game_menu.add_command(label="Coin Flip", command="")
        game_menu.add_command(label="Number Guess", command="")
        game_menu.add_command(label="RPS", command="")
        game_menu.add_command(label="Slots", command="")
        game_menu.add_command(label="TicTacToe", command="")
        game_menu.add_command(label="Trivia", command="")

        # Home menu
        home_menu: tk.Menu = tk.Menu(self.menu_bar, tearoff=False)
        self.menu_bar.add_cascade(label="Home", menu=home_menu)
        home_menu.add_command(label="Main Menu", command="")
        home_menu.add_command(label="Quit", command=self.quit)

        self.configure(menu=self.menu_bar)

    def transition_to_password_reset(self):
        """
        Transitions to PasswordResetFrame
        :return: None
        """
        self.render_frame(PasswordResetFrame)


if __name__ == "__main__":
    app = MainWindow()
    app.mainloop()
