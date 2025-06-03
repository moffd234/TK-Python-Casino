from tkinter import ttk
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from Application.Controller.MainWindow import MainWindow


class BaseFrame(ttk.Frame):
    """
    Parent class of all the frames used in the application.
    """

    def __init__(self, parent: ttk.Frame, controller: 'MainWindow', **kwargs):
        super().__init__(parent)
        self.controller: 'MainWindow' = controller  # Controller should always be a MainWindow object

        self.error_label: ttk.Label = ttk.Label(self, foreground="red")
        self.success_label: ttk.Label = ttk.Label(self, foreground="green")