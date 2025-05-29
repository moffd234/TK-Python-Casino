import tkinter
from tkinter import ttk


class EntryFrame(ttk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller: tkinter.Tk = controller # MainWindow

        self.login_button: ttk.Button = ttk.Button(self, text="Login")
        self.signup_button: ttk.Button = ttk.Button(self, text="Sign Up")

        self.login_button.grid(row=1, column=0, padx=20, pady=20, sticky="e")
        self.signup_button.grid(row=1, column=1, padx=20, pady=20, sticky="w")