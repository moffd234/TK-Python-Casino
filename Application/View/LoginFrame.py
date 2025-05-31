from tkinter import ttk
from typing import TYPE_CHECKING
from Application.Utils.PlaceholderEntry import PlaceholderEntry as pEntry

from Application.Controller.AccountController import AccountController
from Application.View.BaseFrame import BaseFrame

if TYPE_CHECKING:
    from Application.Controller.MainWindow import MainWindow


class LoginFrame(BaseFrame):
    def __init__(self, parent: ttk.Frame, controller: 'MainWindow', account_controller: AccountController) -> None:
        super().__init__(parent, controller)
        self.controller = controller
        self.account_controller = account_controller

        self.username_entry: pEntry = pEntry(self, placeholder="Username", width=50)
        self.password_entry: pEntry = pEntry(self, placeholder="Password", width=50)

        self.login_button: ttk.Button = ttk.Button(self, text="Login", command="")
        self.back_button: ttk.Button = ttk.Button(self, text="Back", command=self.transition_back)

        self.error_label: ttk.Label = ttk.Label(text="Incorrect username or password")  # Hidden until there is an error

        self.place_elements()

    def transition_back(self):
        from Application.View.EntryFrame import EntryFrame
        self.controller.render_frame(EntryFrame)

    def place_elements(self):
        self.username_entry.place(relx=0.5, rely=0.35, anchor="center")
        self.password_entry.place(relx=0.5, rely=0.45, anchor="center")

        self.login_button.place(relx=0.45, rely=0.6, anchor="center")
        self.back_button.place(relx=0.55, rely=0.6, anchor="center")
