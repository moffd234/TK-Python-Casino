import os
from tkinter import ttk, PhotoImage
from PIL import Image, ImageTk
from PIL.Image import Image as PILImage

from Application.Model.GameCard import GameCard
from Application.View.BaseFrame import BaseFrame

ASSETS_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "Assets"))


class GameSelectionFrame(BaseFrame):

    def __init__(self, parent, controller):
        super().__init__(parent, controller)
        self.placeholder_image = ImageTk.PhotoImage(Image.new("RGB", (100, 100), color="gray"))
        self.place_elements()

    def place_elements(self) -> None:
        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(3, weight=1)
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure(2, weight=1)

        title_label = ttk.Label(self, text="Choose A Game", font=("Helvetica", 16, "bold"))
        title_label.grid(row=0, column=0, columnspan=3, pady=20)

        game_cards = [
            GameCard("CoinFlip", os.path.join(ASSETS_PATH, "CoinFlip.png"), 1, 0, self.controller.transition_to_coinflip),
            GameCard("NumberGuess", os.path.join(ASSETS_PATH, "NumberImage.png"), 1, 1, self.controller.transition_to_ng),
            GameCard("RPS", os.path.join(ASSETS_PATH, "RPS_2.png"), 1, 2, self.controller.transition_to_rps),
            GameCard("Slots", os.path.join(ASSETS_PATH, "Slots.png"), 2, 0, self.controller.transition_to_slots),
            GameCard("TicTacToe", os.path.join(ASSETS_PATH, "TicTacToe.png"), 2, 1, self.controller.transition_to_ttt),
            GameCard("Trivia", os.path.join(ASSETS_PATH, "Trivia.png"), 2, 2, self.controller.transition_to_trivia),
        ]

        for game in game_cards:
            frame = ttk.Frame(self)
            frame.grid(row=game.row, column=game.col, padx=20, pady=20, sticky="nsew")

            img: PILImage = Image.open(game.image_path)
            img = img.resize((100, 100), Image.Resampling.LANCZOS)
            tk_image: PhotoImage = ImageTk.PhotoImage(img)

            img_button = ttk.Button(frame, image=tk_image, command=game.callback)
            img_button.image = tk_image
            img_button.pack()

            text_label = ttk.Label(frame, text=game.name, font=("Helvetica", 10, "bold"))
            text_label.pack()