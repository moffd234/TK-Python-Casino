import tkinter
from tkinter import ttk

from Application.View.BaseFrame import BaseFrame


class EntryFrame(BaseFrame):
    def __init__(self, parent, controller):
        super().__init__(parent, controller)
        self.controller: tkinter.Tk = controller  # MainWindow

        self.login_button: ttk.Button = ttk.Button(self, text="Login", command=self.login)
        self.signup_button: ttk.Button = ttk.Button(self, text="Sign Up", command=self.signup)

        self.login_button.grid(row=1, column=0, padx=20, pady=20, sticky="e")
        self.signup_button.grid(row=1, column=1, padx=20, pady=20, sticky="w")

    def login(self) -> None:
        pass

    def signup(self) -> None:
        pass
