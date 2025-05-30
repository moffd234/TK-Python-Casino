import tkinter
from tkinter import ttk

from Application.Controller.MainWindow import MainWindow


class BaseFrame(ttk.Frame):
    """
    Parent class of all the frames used in the application.
    """

    def __init__(self, parent: ttk.Frame, controller: MainWindow):
        super().__init__(parent)
        self.controller: tkinter.Tk = controller  # Controller should always be a MainWindow object
