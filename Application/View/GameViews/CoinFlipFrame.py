import logging
import os
import tkinter.messagebox
from tkinter import ttk, PhotoImage
from PIL import Image, ImageTk
from PIL.Image import Image as PILImage

from Application.Model.Games.GameOutcome import GameOutcome
from Application.Utils.TypeValidation import validate_float
from Application.View.BaseFrame import BaseFrame


class CoinFlipFrame(BaseFrame):

    def __init__(self, parent, controller):
        super().__init__(parent, controller)

        ASSETS_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../Assets"))
        tails_image_path = os.path.join(ASSETS_PATH, "cs_tails.png")
        heads_image_path = os.path.join(ASSETS_PATH, "cs_heads.png")

        img: PILImage = Image.open(tails_image_path).resize((100, 100), Image.Resampling.LANCZOS)
        self.tails_image: PhotoImage = ImageTk.PhotoImage(img)
        self.tails_button: ttk.Button = ttk.Button(self, image=self.tails_image, command=self.tails_chosen)

        img = Image.open(heads_image_path).resize((100, 100), Image.Resampling.LANCZOS)
        self.heads_image: PhotoImage = ImageTk.PhotoImage(img)
        self.heads_button: ttk.Button = ttk.Button(self, image=self.heads_image, command=self.heads_chosen)

        self.prompt_label: ttk.Label = ttk.Label(self, text="Choose A Coin Side", font=("Helvetica", 16, "bold"))
        self.wager_label: ttk.Label = ttk.Label(self, text="Enter Wager:", font=("Helvetica", 12))

        validate = (self.register(validate_float), "%P")
        self.wager_entry: ttk.Entry = ttk.Entry(self, width=20, validate="key", validatecommand=validate)

        self.place_elements()

    def place_elements(self):
        self.prompt_label.place(relx=0.5, rely=0.15, anchor="center")
        self.wager_label.place(relx=0.5, rely=0.25, anchor="center")
        self.wager_entry.place(relx=0.5, rely=0.30, anchor="center")

        self.tails_button.place(relx=0.35, rely=0.45, anchor="center")
        self.heads_button.place(relx=0.65, rely=0.45, anchor="center")

    def tails_chosen(self) -> None:
        """
        Handles event for when user selects the tails coin
        :return: None
        """
        self.coin_selected("tails")

    def heads_chosen(self) -> None:
        """
        Handles event for when user selects the heads coin
        :return: None
        """
        self.coin_selected("heads")

    def handle_outcome(self, outcome: GameOutcome, wager: float) -> None:
        """
        Displays the result of the coin flip game to the user based on the outcome.
        :param outcome: The result of the coin flip (WIN, LOSS, or WITHDRAW_ERROR).
        :param wager: The amount the user wagered.
        :return: None
        """

        if outcome == GameOutcome.WIN:
            self.success_label.config(text=f"You Won! Your winnings are ${wager * 0.25}")
            self.success_label.place(relx=0.5, rely=0.15, anchor="center")
        elif outcome == GameOutcome.LOSS:
            self.error_label.config(text="You loss!")
            self.error_label.place(relx=0.5, rely=0.15, anchor="center")

        else:
            self.error_label.config(text="You do not have enough balance for that wager")
            self.error_label.place(relx=0.5, rely=0.15, anchor="center")

    def coin_selected(self, guess: str) -> None:
        self.success_label.place_forget()
        self.error_label.place_forget()
        self.prompt_label.place_forget()

        try:
            wager: float = float(self.wager_entry.get())
            outcome: GameOutcome = self.controller.game_controller.cf_controller.handle_outcome(guess, wager)

            self.handle_outcome(outcome, wager)

        except ValueError:
            tkinter.messagebox.showerror(message="An error has occurred. Try again")
            logging.error("Error casting wager to float in CoinFlip")
