from Application.Model.Accounts.AccountManager import AccountManager


class LoginController:
    def __init__(self, manager: AccountManager):
        self.manager = manager