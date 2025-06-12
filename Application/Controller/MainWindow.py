import tkinter as tk
from tkinter import ttk

from Application.Controller.AccountController import AccountController
from Application.Utils.LoggingController import setup_logging
from Application.Model.Accounts.AccountManager import AccountManager
from Application.View.BaseFrame import BaseFrame
from Application.View.EntryFrame import EntryFrame

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
        self.create_menu()

        self.render_frame(EntryFrame)
        # self.render_frame(MainMenuFrame)

    def render_frame(self, new_frame: type[BaseFrame], **kwargs) -> None:
        """
        Destroys previous frame and renders new frame.
        :param new_frame: A new Frame object.
        :return: None
        """
        for frame in self.container.winfo_children():
            frame.destroy()

        frame: ttk.Frame = new_frame(self.container, self, **kwargs)
        frame.pack(fill="both", expand=True)

    def create_menu(self):
        menu_bar: tk.Menu = tk.Menu()

        # Account Menu
        account_menu: tk.Menu = tk.Menu(menu_bar, tearoff=False)
        menu_bar.add_cascade(label="Account", menu=account_menu)

        # Game Menu
        game_menu: tk.Menu = tk.Menu(menu_bar, tearoff=False)
        menu_bar.add_cascade(label="Games", menu=game_menu)

        self.configure(menu=menu_bar)

if __name__ == "__main__":
    app = MainWindow()
    app.mainloop()
