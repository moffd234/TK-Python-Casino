from tkinter import ttk

from Application.View.BaseFrame import BaseFrame


class MainMenuFrame(BaseFrame):

    def __init__(self, parent, controller):
        super().__init__(parent, controller)
        self.controller = controller
        self.play_game_button: ttk.Button = ttk.Button(text="Play", width=15, command=self.transition_to_game_screen)
        self.manage_account_button: ttk.Button = ttk.Button(text="Manage Account", width=15,
                                                            command=self.transition_to_account_management)
        self.logout_button: ttk.Button = ttk.Button(text="Logout", width=15, command=self.logout_user)

        style: ttk.Style = ttk.Style()
        style.configure(style="Title.TLabel", font=("TkDefaultFont", 25))
        self.title_label: ttk.Label = ttk.Label(text="Select an action", style="Title.TLabel")

        self.place_elements()

    def place_elements(self) -> None:
        self.title_label.place(relx=0.5, rely=0.2, anchor="center")

        self.play_game_button.place(relx=0.4, rely=0.5, anchor="center")
        self.manage_account_button.place(relx=0.6, rely=0.5, anchor="center")
        self.logout_button.place(relx=0.5, rely=0.6, anchor="center")

    def transition_to_game_screen(self) -> None:
        pass

    def transition_to_account_management(self) -> None:
        pass

    def logout_user(self) -> None:
        from Application.View.EntryFrame import EntryFrame

        self.controller.account_controller.account = None
        self.controller.render_frame(EntryFrame)
