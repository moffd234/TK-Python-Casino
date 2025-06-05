from tkinter import ttk
from typing import TYPE_CHECKING

from Application.Controller.AccountController import is_password_valid
from Application.Utils.PlaceholderEntry import PlaceholderEntry as pEntry
from Application.View.BaseFrame import BaseFrame

if TYPE_CHECKING:
    from Application.Controller.MainWindow import MainWindow


class PasswordResetFrame(BaseFrame):
    def __init__(self, parent: ttk.Frame, controller: 'MainWindow'):
        super().__init__(parent, controller)

        style: ttk.Style = ttk.Style()
        style.configure(style="Title.TLabel", font=("TkDefaultFont", 25))
        self.info_label: ttk.Label = ttk.Label(text="Enter your new password.", style="Title.TLabel")

        self.password_entry: pEntry = pEntry(self, "Enter New Password", width=50)
        self.confirm_entry: pEntry = pEntry(self, "Confirm Password", width=50)

        self.reset_button: ttk.Button = ttk.Button(self, text="Reset", command=self.reset_password)
        self.back_button: ttk.Button = ttk.Button(self, text="Back", command="")

        self.place()

    def place(self) -> None:
        self.info_label.place(relx=0.5, rely=0.35, anchor="center")
        self.password_entry.place(relx=0.5, rely=0.45, anchor="center")
        self.confirm_entry.place(relx=0.5, rely=0.55, anchor="center")
        self.reset_button.place(relx=0.4, rely=0.65, anchor="center")
        self.back_button.place(relx=0.6, rely=0.65, anchor="center")

    def reset_password(self) -> None:
        new_password: str = self.password_entry.get()
        confirm_password = self.confirm_entry.get()

        if new_password != confirm_password:
            self.error_label.configure(text="Passwords do not match.")
            self.error_label.place(relx=0.5, rely=0.2, anchor="center")
            return

        if not is_password_valid(new_password):
            self.error_label.configure(text="Invalid Password")
            self.error_label.place(relx=0.5, rely=0.2, anchor="center")
            return

        self.controller.account_controller.reset_password(new_password)
