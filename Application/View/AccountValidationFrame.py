from tkinter import ttk
from typing import TYPE_CHECKING

from Application.Model.Accounts.UserAccount import UserAccount
from Application.Utils.PlaceholderEntry import PlaceholderEntry as pEntry
from Application.View.BaseFrame import BaseFrame
from Application.View.EntryFrame import EntryFrame
from Application.View.LoginFrame import LoginFrame
from Application.View.PasswordResetFrame import PasswordResetFrame

if TYPE_CHECKING:
    from Application.Controller.MainWindow import MainWindow


class AccountValidationFrame(BaseFrame):
    def __init__(self, parent: ttk.Frame, controller: 'MainWindow'):
        super().__init__(parent, controller)
        self.controller: 'MainWindow' = controller
        self.account: None | UserAccount = None

        self.email_entry: pEntry = pEntry(self, "Email", width=50)
        self.answer_one_entry: pEntry = pEntry(self, "Answer", width=50)
        self.answer_two_entry: pEntry = pEntry(self, "Answer", width=50)
        self.auth_entry: pEntry = pEntry(self, "Auth Token", width=50)

        self.error_label = ttk.Label(self, foreground="red")
        self.answer_one_label = ttk.Label(self)
        self.answer_two_label = ttk.Label(self)

        self.validate_button: ttk.Button = ttk.Button(self, text="Validate", command=self.get_account_from_email)
        self.back_button: ttk.Button = ttk.Button(self, text="Back", command=self.transition_back)

        self.place()

    def place(self) -> None:
        self.email_entry.place(relx=0.5, rely=0.5, anchor="center")
        self.validate_button.place(relx=0.4, rely=0.65, anchor="center")
        self.back_button.place(relx=0.6, rely=0.65, anchor="center")

    def get_account_from_email(self) -> None:
        self.account: UserAccount = self.controller.account_controller.validate_email(self.email_entry.get())
        if not self.account:
            self.error_label.configure(text="Invalid email")
            self.error_label.place(relx=0.5, rely=0.15, anchor="center")

        else:
            self.email_entry.place_forget()
            self.validate_button.configure(command=self.validate_security_answers)
            self.place_security_questions()

    def place_security_questions(self) -> None:
        self.answer_one_label.configure(text=self.account.security_question_one)
        self.answer_two_label.configure(text=self.account.security_question_two)

        self.answer_one_label.place(relx=0.5, rely=0.2, anchor="center")
        self.answer_one_entry.place(relx=0.5, rely=0.3, anchor="center")

        self.answer_two_label.place(relx=0.5, rely=0.4, anchor="center")
        self.answer_two_entry.place(relx=0.5, rely=0.5, anchor="center")

    def validate_security_answers(self) -> None:
        if (self.answer_one_entry.get() == self.account.security_answer_one
                and self.answer_two_entry.get() == self.account.security_answer_two):
            self.controller.account_controller.email_reset_token()

            # Clear security prompts
            self.answer_one_entry.place_forget()
            self.answer_two_entry.place_forget()
            self.answer_one_label.place_forget()
            self.answer_two_label.place_forget()

            self.validate_button.configure(command=self.validate_auth_token)

            self.place_auth_token()
        else:
            self.error_label.configure(text="Incorrect security answers")

    def place_auth_token(self) -> None:
        self.error_label.configure(text="Auth Token Has Been Emailed", foreground="green")
        self.error_label.place(relx=0.5, rely=0.15, anchor="center")
        self.auth_entry.place(relx=0.5, rely=0.5, anchor="center")

    def validate_auth_token(self) -> None:
        if self.auth_entry.get().strip() == str(self.account.reset_token):
            self.controller.render_frame(PasswordResetFrame)
        else:
            self.error_label.configure(text="Incorrect auth token", foreground="red")
            self.error_label.place()

    def transition_back(self):
        self.controller.render_frame(LoginFrame)