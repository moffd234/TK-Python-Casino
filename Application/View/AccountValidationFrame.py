from tkinter import ttk
from typing import TYPE_CHECKING

from Application.Controller.MainWindow import MainWindow
from Application.Model.Accounts.UserAccount import UserAccount
from Application.Utils.PlaceholderEntry import PlaceholderEntry as pEntry
from Application.View.BaseFrame import BaseFrame

if TYPE_CHECKING:
    from Application.Controller.MainWindow import MainWindow


class AccountValidationFrame(BaseFrame):
    def __init__(self, parent: ttk.Frame, controller: 'MainWindow'):
        super().__init__(parent, controller)
        self.controller: 'MainWindow' = controller

        self.email_entry: pEntry = pEntry(self, "Email")
        self.answer_one: pEntry = pEntry(self, "Answer")
        self.answer_two: pEntry = pEntry(self, "Answer")

        self.error_label = ttk.Label(parent)
        self.answer_one_label = ttk.Label(parent)
        self.answer_two_label = ttk.Label(parent)

        self.validate_button: ttk.Button = ttk.Button(self, text="Validate", command=self.validate_email)
        self.back_button: ttk.Button = ttk.Button(self, text="Back")

        self.place()

    def place(self):
        self.email_entry.place(relx=0.5, rely=0.5, anchor="center")
        self.validate_button.place(relx=0.4, rely=0.65, anchor="center")
        self.back_button.place(relx=0.6, rely=0.65, anchor="center")

    def get_account_from_email(self):
        account: UserAccount = self.controller.account_controller.validate_email(self.email_entry.get())
        if not account:
            self.error_label.configure(text="Invalid email", foreground="red")
            self.error_label.place(relx=0.5, rely=0.15, anchor="center")

        else:
            self.validate_button.configure(command=self.validate_security_answers)
            self.place_security_questions()


    def place_security_questions(self):
        pass

    def validate_security_answers(self):
        pass