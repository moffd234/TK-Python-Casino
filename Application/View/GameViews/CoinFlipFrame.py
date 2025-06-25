import os
from tkinter import ttk, PhotoImage
from PIL import Image, ImageTk
from PIL.Image import Image as PILImage

from Application.View.BaseFrame import BaseFrame


class CoinFlipFrame(BaseFrame):

    def __init__(self, parent, controller):
        super().__init__(parent, controller)

        ASSETS_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../Assets"))
        tails_image_path = os.path.join(ASSETS_PATH, "cs_tails.png")
        heads_image_path = os.path.join(ASSETS_PATH, "cs_heads.png")

        img: PILImage = Image.open(tails_image_path).resize((100, 100), Image.Resampling.LANCZOS)
        self.tails_image: PhotoImage = ImageTk.PhotoImage(img)
        self.tails_button: ttk.Button = ttk.Button(self, image=self.tails_image, command="")

        img = Image.open(heads_image_path).resize((100, 100), Image.Resampling.LANCZOS)
        self.heads_image: PhotoImage = ImageTk.PhotoImage(img)
        self.heads_button: ttk.Button = ttk.Button(self, image=self.heads_image, command="")

        self.prompt_label: ttk.Label = ttk.Label(self, text="Choose A Coin Side", font=("Helvetica", 16, "bold"))

        self.place_elements()

    def place_elements(self):
        pass
