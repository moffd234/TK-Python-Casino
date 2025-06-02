from tkinter import ttk
from typing import TYPE_CHECKING

from Application.Controller.MainWindow import MainWindow
from Application.View.BaseFrame import BaseFrame

if TYPE_CHECKING:
    from Application.Controller.MainWindow import MainWindow


class PasswordResetFrame(BaseFrame):
    def __init__(self, parent: ttk.Frame, controller: 'MainWindow', from_login: bool=True):
        super().__init__(parent, controller)
        self.controller: 'MainWindow' = controller
        self.from_login: bool = from_login

