from tkinter import ttk
from typing import TYPE_CHECKING

from Application.Casino.Casino import is_password_valid, is_email_valid
from Application.Utils.PlaceholderEntry import PlaceholderEntry as pEntry
from Application.View.BaseFrame import BaseFrame
from Application.View.EntryFrame import EntryFrame
from Application.View.MainMenuFrame import MainMenuFrame

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

        self.security_question_one: ttk.Combobox = ttk.Combobox(self, values=possible_questions, state="readonly",
                                                                width=60)
        self.security_question_two: ttk.Combobox = ttk.Combobox(self, values=possible_questions, state="readonly",
                                                                width=60)
        self.security_question_one.set(possible_questions[0])
        self.security_question_two.set(possible_questions[1])

        self.signup: ttk.Button = ttk.Button(self, text="Signup", command=self.signup)
        self.back_button: ttk.Button = ttk.Button(self, text="Back", command=self.transition_back)

        self.elements: list = [self.username_entry, self.password_entry, self.email_entry,
                               self.security_entry_one, self.security_entry_two]

        self.place_elements()

    def place_elements(self) -> None:
        vertical_spacing = 0.08
        base_y = 0.28

        self.username_entry.place(relx=0.5, rely=base_y, anchor="center")
        self.email_entry.place(relx=0.5, rely=base_y + vertical_spacing, anchor="center")
        self.password_entry.place(relx=0.5, rely=base_y + vertical_spacing * 2, anchor="center")

        self.security_question_one.config(width=60)
        self.security_question_two.config(width=60)

        self.security_question_one.place(relx=0.5, rely=base_y + vertical_spacing * 3.2, anchor="center")
        self.security_entry_one.place(relx=0.5, rely=base_y + vertical_spacing * 3.9, anchor="center")

        self.security_question_two.place(relx=0.5, rely=base_y + vertical_spacing * 4.6, anchor="center")
        self.security_entry_two.place(relx=0.5, rely=base_y + vertical_spacing * 5.3, anchor="center")

        self.signup.place(relx=0.42, rely=base_y + vertical_spacing * 6.2, anchor="center")
        self.back_button.place(relx=0.58, rely=base_y + vertical_spacing * 6.2, anchor="center")

    def validate_fields(self) -> tuple[bool, str | None]:
        """
        Validates that all required fields in the sign-up form are properly filled.

        This includes:
        - Ensuring no fields are left blank or contain only whitespace.
        - Ensuring the two selected security questions are different.
        - Validating that the password meets complexity requirements.
        - Validating the format of the provided email address.

        :return: A tuple (is_valid, error_message):
            - is_valid (bool): True if all validations pass, otherwise False.
            - error_message (str | None): The associated error message if validation fails, or None if successful.
        """

        for element in self.elements:
            if element.get_real_value() == "":
                return False, "All Fields Must Be Filled"

        if self.security_question_one.get() == self.security_question_two.get():
            return False, "Security Answers Must Be Different"

        if not is_password_valid(self.password_entry.get()):
            return False, ("Password must include 1 special character,"
                           " 1 number, 1 lowercase letter and 1 uppercase letter")

        if not is_email_valid(self.email_entry.get()):
            return False, "Email Must Be Valid"

        return True, None

    def signup(self) -> None:
        """
        Handles the sign-up process for a new user.

        This method performs the following:
        - Validates that all required fields are filled and correctly formatted.
        - Extracts user input from form fields.
        - Sends the data to the AccountController to attempt account creation.
        - Displays an error message if validation or account creation fails.
        - Transitions to the MainMenuFrame upon successful sign-up.

        :return: None
        """
        self.error_label.place_forget()
        is_valid, error_message = self.validate_fields()

        if not is_valid:
            self.error_label.config(text=error_message)
            self.error_label.place(relx=0.5, rely=0.15, anchor="center")
            return

        username: str = self.username_entry.get_real_value().strip()
        password: str = self.password_entry.get_real_value().strip()
        email: str = self.email_entry.get_real_value().strip()
        questions: list[str] = [self.security_question_one.get().strip(), self.security_entry_one.get().strip(),
                                self.security_question_two.get().strip(), self.security_entry_two.get().strip()]

        is_valid, error_message = self.controller.account_controller.create_account(username, password, email, questions)

        if not is_valid:
            self.error_label.config(text=error_message)
            self.error_label.place(relx=0.5, rely=0.15, anchor="center")
            return

        self.controller.render_frame(MainMenuFrame)

    def transition_back(self) -> None:
        """
        Transitions user back to the EntryFrame
        :return: None
        """
        self.controller.render_frame(EntryFrame)