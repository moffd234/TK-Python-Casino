from tkinter import ttk
from typing import TYPE_CHECKING

from Application.View.BaseFrame import BaseFrame

if TYPE_CHECKING:
    from Application.Controller.MainWindow import MainWindow

class SignUpFrame(BaseFrame):

    def __init__(self, parent: ttk.Frame, controller: 'MainWindow'):
        super().__init__(parent, controller)
        self.controller: 'MainWindow' = controller