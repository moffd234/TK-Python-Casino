from tkinter import ttk
from typing import TYPE_CHECKING
from Application.Utils.PlaceholderEntry import PlaceholderEntry as pEntry

from Application.Controller.AccountController import AccountController
from Application.View.BaseFrame import BaseFrame

if TYPE_CHECKING:
    from Application.Controller.MainWindow import MainWindow


class LoginFrame(BaseFrame):
    def __init__(self, parent: ttk.Frame, controller: 'MainWindow', login_controller: AccountController) -> None:
        super().__init__(parent, controller)
        self.controller = controller
        self.login_controller = login_controller

        self.username_entry: pEntry = pEntry(placeholder="Username", width=50)