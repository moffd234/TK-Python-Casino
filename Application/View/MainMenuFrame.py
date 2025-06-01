from Application.View.BaseFrame import BaseFrame


class MainMenuFrame(BaseFrame):

    def __init__(self, parent, controller):
        super().__init__(parent, controller)
        self.controller = controller

