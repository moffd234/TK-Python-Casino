from tkinter import ttk
from typing import TYPE_CHECKING

from Application.Controller.LoginController import LoginController
from Application.View.BaseFrame import BaseFrame

if TYPE_CHECKING:
    from Application.Controller.MainWindow import MainWindow


class LoginFrame(BaseFrame):
    def __init__(self, parent: ttk.Frame, controller: 'MainWindow', login_controller: LoginController) -> None:
        super().__init__(parent, controller)
        self.controller = controller
        self.login_controller = login_controller