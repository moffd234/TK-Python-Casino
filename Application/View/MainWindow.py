import tkinter
from tkinter import ttk


class MainWindow(tkinter.Tk):
    def __init__(self):
        super().__init__()
        self.title("Python Casino!")
        self.geometry("800x800")

        self.container: ttk.Frame = ttk.Frame(self)
        self.container.pack(fill="both", expand=True)

