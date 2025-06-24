from tkinter import ttk, PhotoImage
from PIL import Image, ImageTk
from PIL.Image import Image as PILImage

from Application.View.BaseFrame import BaseFrame


class CoinFlipFrame(BaseFrame):

    def __init__(self, parent, controller):
        super().__init__(parent, controller)

        img: PILImage = Image.open("../../Assets/cs_tails.png").resize((100, 100), Image.Resampling.LANCZOS)
        tails_image: PhotoImage = ImageTk.PhotoImage(img)
        self.tails_button: ttk.Button = ttk.Button(self, image=tails_image, command="")

        img = Image.open("../../Assets/cs_heads.png").resize((100, 100), Image.Resampling.LANCZOS)
        heads_image: PhotoImage = ImageTk.PhotoImage(img)
        self.tails_button: ttk.Button = ttk.Button(self, image=heads_image, command="")

        self.prompt_label: ttk.Label = ttk.Label(self, text="Choose A Coin Side", font=("Helvetica", 16, "bold"))

    def place_elements(self):
        pass
