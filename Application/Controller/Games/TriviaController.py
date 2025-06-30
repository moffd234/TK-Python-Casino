from Application.Controller.AccountController import AccountController


class TriviaController:

    def __init__(self, account_controller: AccountController):
        self.account_controller: AccountController = account_controller

