from tkinter import ttk
from typing import TYPE_CHECKING
from Application.Utils.PlaceholderEntry import PlaceholderEntry as pEntry

from Application.View.BaseFrame import BaseFrame
from Application.View.MainMenuFrame import MainMenuFrame

if TYPE_CHECKING:
    from Application.Controller.MainWindow import MainWindow


class LoginFrame(BaseFrame):
    def __init__(self, parent: ttk.Frame, controller: 'MainWindow') -> None:
        super().__init__(parent, controller)
        self.controller = controller

        self.username_entry: pEntry = pEntry(self, placeholder="Username", width=50)
        self.password_entry: pEntry = pEntry(self, placeholder="Password", width=50)

        self.reset_password_button: ttk.Button = ttk.Button(self, text="Reset Password",
                                                            command=self.transition_to_validation)
        self.login_button: ttk.Button = ttk.Button(self, text="Login", command=self.login)
        self.back_button: ttk.Button = ttk.Button(self, text="Back", command=self.transition_back)

        # Do not place this until error occurs
        self.error_label: ttk.Label = ttk.Label(self, text="Incorrect username or password", foreground="red")

        self.place_elements()

    def login(self) -> None:
        username: str = self.username_entry.get()
        password: str = self.password_entry.get()

        account: bool = self.controller.account_controller.login(username, password)

        if account:
            self.controller.render_frame(MainMenuFrame)

        else:
            self.error_label.place(relx=0.5, rely=0.5, anchor="center")

    def transition_back(self) -> None:
        from Application.View.EntryFrame import EntryFrame
        self.controller.render_frame(EntryFrame)

    def transition_to_validation(self) -> None:
        from Application.View.AccountValidationFrame import AccountValidationFrame
        self.controller.render_frame(AccountValidationFrame)

    def place_elements(self) -> None:
        self.username_entry.place(relx=0.5, rely=0.35, anchor="center")
        self.password_entry.place(relx=0.5, rely=0.45, anchor="center")

        self.login_button.place(relx=0.45, rely=0.6, anchor="center")
        self.back_button.place(relx=0.55, rely=0.6, anchor="center")
        self.reset_password_button.place(relx=0.5, rely=0.68, anchor="center")
