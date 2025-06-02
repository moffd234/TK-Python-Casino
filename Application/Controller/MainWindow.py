import tkinter
from tkinter import ttk

from Application.Controller.AccountController import AccountController
from Application.Model.Accounts.AccountManager import AccountManager
from Application.View.BaseFrame import BaseFrame
from Application.View.EntryFrame import EntryFrame


class MainWindow(tkinter.Tk):
    def __init__(self):
        super().__init__()
        self.title("Python Casino!")
        self.geometry("800x800")
        account_manager: AccountManager = AccountManager()
        self.account_controller: AccountController = AccountController(account_manager)

        self.container: ttk.Frame = ttk.Frame(self)
        self.container.pack(fill="both", expand=True)

        self.render_frame(EntryFrame)

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

if __name__ == "__main__":
    app = MainWindow()
    app.mainloop()
