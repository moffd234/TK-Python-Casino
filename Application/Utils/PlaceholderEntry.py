from tkinter import ttk


class PlaceholderEntry(ttk.Entry):
    def __init__(self, master=None, placeholder="", color='grey'):
        super().__init__(master)
        self.placeholder = placeholder
        self.color = color