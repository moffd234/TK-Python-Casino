import tkinter
from tkinter import ttk

from Application.View.BaseFrame import BaseFrame
from Application.View.EntryFrame import EntryFrame


class MainWindow(tkinter.Tk):
    def __init__(self):
        super().__init__()
        self.title("Python Casino!")
        self.geometry("800x800")

        self.container: ttk.Frame = ttk.Frame(self)
        self.container.pack(fill="both", expand=True)

        self.render_frame(EntryFrame)

    def render_frame(self, new_frame: type[BaseFrame]) -> None:
        """
        Destroys previous frame and renders new frame.
        :param new_frame: A new Frame object.
        :return: None
        """
        for frame in self.container.winfo_children():
            frame.destroy()

        frame: ttk.Frame = new_frame(self.container, self)
        frame.pack(fill="both", expand=True)

if __name__ == "__main__":
    app = MainWindow()
    app.mainloop()
