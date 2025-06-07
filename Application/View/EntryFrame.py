from tkinter import ttk
from typing import TYPE_CHECKING

from Application.View.BaseFrame import BaseFrame
from Application.View.LoginFrame import LoginFrame
from Application.View.SignUpFrame import SignUpFrame

if TYPE_CHECKING:
    from Application.Controller.MainWindow import MainWindow


class EntryFrame(BaseFrame):
    def __init__(self, parent: ttk.Frame, controller: 'MainWindow'):
        super().__init__(parent, controller)
        self.controller: 'MainWindow' = controller  # MainWindow

        self.login_button: ttk.Button = ttk.Button(self, text="Login", command=self.login)
        self.signup_button: ttk.Button = ttk.Button(self, text="Sign Up", command=self.signup)

        style: ttk.Style = ttk.Style()
        style.configure(style="Title.TLabel", font=("TkDefaultFont", 25))
        self.title_label: ttk.Label = ttk.Label(self, text="Welcome to Python Casino 🎰🎰🎰", style="Title.TLabel")

        self.place_elements()


    def login(self) -> None:
        self.controller.render_frame(LoginFrame)

    def signup(self) -> None:
        self.controller.render_frame(SignUpFrame)

    def place_elements(self):
        self.title_label.place(relx=0.5, rely=0.25, anchor="center")
        self.login_button.place(relx=0.4, rely=0.5, anchor="center")
        self.signup_button.place(relx=0.6, rely=0.5, anchor="center")