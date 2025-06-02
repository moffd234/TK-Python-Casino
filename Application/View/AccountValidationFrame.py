from tkinter import ttk
from typing import TYPE_CHECKING

from Application.Controller.MainWindow import MainWindow
from Application.Utils.PlaceholderEntry import PlaceholderEntry as pEntry
from Application.View.BaseFrame import BaseFrame

if TYPE_CHECKING:
    from Application.Controller.MainWindow import MainWindow


class AccountValidationFrame(BaseFrame):
    def __init__(self, parent: ttk.Frame, controller: 'MainWindow'):
        super().__init__(parent, controller)
        self.controller: 'MainWindow' = controller

        self.email_entry: pEntry = pEntry(self, "Email")

        self.error_label = ttk.Label(parent)

        self.validate_button: ttk.Button = ttk.Button(self, text="Validate")
        self.back_button: ttk.Button = ttk.Button(self, text="Back")

        self.place()

    def place(self):
        self.email_entry.place(relx=0.5, rely=0.5, anchor="center")
        self.validate_button.place(relx=0.4, rely=0.65, anchor="center")
        self.back_button.place(relx=0.6, rely=0.65, anchor="center")

    def validate_email(self):
        pass