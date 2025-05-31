import tkinter


class PlaceholderEntry(tkinter.Entry):
    def __init__(self, master=None, placeholder="", color='grey'):
        super().__init__(master)
        self.placeholder: str = placeholder
        self.color: str = color
        self.default_fg_color: str = self.cget('foreground')

        # Bind functions on FocusIn and FocusOut
        self.bind("<FocusIn>", self.focus_in)
        self.bind("<FocusOut>", self.focus_out)