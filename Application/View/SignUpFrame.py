from tkinter import ttk
from typing import TYPE_CHECKING

from Application.Utils.PlaceholderEntry import PlaceholderEntry as pEntry
from Application.View.BaseFrame import BaseFrame

if TYPE_CHECKING:
    from Application.Controller.MainWindow import MainWindow


class SignUpFrame(BaseFrame):

    def __init__(self, parent: ttk.Frame, controller: 'MainWindow'):
        super().__init__(parent, controller)
        self.controller: 'MainWindow' = controller

        possible_questions: list[str] = [
            "What is your favorite sports team?",
            "What street did you grow up on?",
            "What was the name of your first pet?",
            "What is your mother’s maiden name?",
            "What was the name of your elementary school?",
            "In what city were you born?",
            "What was the make of your first car?",
            "What is your favorite movie?",
            "What is your childhood best friend's first name?",
            "What was the name of your first employer?",
            "What is your favorite food?",
            "What is the name of your favorite teacher?",
            "Where did you go on your first vacation?",
            "What is the middle name of your oldest sibling?",
            "What was the name of your first stuffed animal?"
        ]

        self.username_entry: pEntry = pEntry(self, "Username", width=50)
        self.password_entry: pEntry = pEntry(self, "Password", width=50)
        self.email_entry: pEntry = pEntry(self, "Email", width=50)
        self.security_entry_one: pEntry = pEntry(self, "Security Answer", width=50)
        self.security_entry_two: pEntry = pEntry(self, "Security Answer", width=50)

        self.security_question_one: ttk.Combobox = ttk.Combobox(self, values=possible_questions, state="readonly", width=60)
        self.security_question_two: ttk.Combobox = ttk.Combobox(self, values=possible_questions, state="readonly", width=60)

        self.reset_button: ttk.Button = ttk.Button(self, text="Signup", command="")
        self.back_button: ttk.Button = ttk.Button(self, text="Back", command="")
