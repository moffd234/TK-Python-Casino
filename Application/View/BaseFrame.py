from abc import ABC, abstractmethod
from tkinter import ttk
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from Application.Controller.MainWindow import MainWindow


class BaseFrame(ttk.Frame, ABC):
    """
    Parent class of all the frames used in the application.

    Naming conventions:
        All classes should be named <ScreenDescriptor>Frame
        Any function that's sole purpose is to transitions screens should be named transition_to_<NEW_SCREEN_DESCRIPTOR>
    """

    def __init__(self, parent: ttk.Frame, controller: 'MainWindow', **kwargs):
        super().__init__(parent)
        self.controller: 'MainWindow' = controller  # Controller should always be a MainWindow object

        self.error_label: ttk.Label = ttk.Label(self, foreground="red")
        self.success_label: ttk.Label = ttk.Label(self, foreground="green")

    @abstractmethod
    def place_elements(self):
        pass