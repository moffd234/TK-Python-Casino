class GameCard:

    def __init__(self, name, image_path, row, col, callback):
        self.name = name
        self.image_path = image_path
        self.row = row
        self.col = col
        self.callback = callback
