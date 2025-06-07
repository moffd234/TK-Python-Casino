from tkinter import ttk

from Application.View.BaseFrame import BaseFrame


class MainMenuFrame(BaseFrame):

    def __init__(self, parent, controller):
        super().__init__(parent, controller)
        self.controller = controller
        self.play_game_button: ttk.Button = ttk.Button(text="Play")
        self.manage_account_button: ttk.Button = ttk.Button(text="Manage Account")
        self.logout_button: ttk.Button = ttk.Button(text="Logout")

        style: ttk.Style = ttk.Style()
        style.configure(style="Title.TLabel", font=("TkDefaultFont", 25))
        self.title_label: ttk.Label = ttk.Label(text="Select an action", style="Title.TLabel")

    def place_elements(self):
        pass
