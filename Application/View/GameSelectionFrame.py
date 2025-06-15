from tkinter import ttk
from PIL import Image, ImageTk
from Application.View.BaseFrame import BaseFrame


class GameSelectionFrame(BaseFrame):

    def __init__(self, parent, controller):
        super().__init__(parent, controller)
        self.placeholder_image = ImageTk.PhotoImage(Image.new("RGB", (100, 100), color="gray"))
        self.place_elements()

    def place_elements(self):
        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(3, weight=1)
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure(2, weight=1)

        title_label = ttk.Label(self, text="Choose A Game", font=("Helvetica", 16, "bold"))
        title_label.grid(row=0, column=0, columnspan=3, pady=20)

        games = [("CoinFlip", 1, 0), ("NumberGuess", 1, 1), ("RPS", 1, 2), ("Slots", 2, 0),
                 ("TicTacToe", 2, 1), ("Trivia", 2, 2)]

        for game_name, row, col in games:
            frame = ttk.Frame(self)
            frame.grid(row=row, column=col, padx=20, pady=20, sticky="nsew")

            img_label = ttk.Label(frame, image=self.placeholder_image)
            img_label.image = self.placeholder_image
            img_label.pack()

            text_label = ttk.Label(frame, text=game_name, font=("Helvetica", 10, "bold"))
            text_label.pack()
