from Application.Model.Accounts.AccountManager import AccountManager
from Application.Model.Accounts.UserAccount import UserAccount


class AccountController:
    def __init__(self, manager: AccountManager):
        self.manager: AccountManager = manager
        self.account: UserAccount | None = None

    def login(self, username: str, password: str) -> UserAccount | None:
        """
        Attempts to authenticate a user with the given credentials

        :param username: Username entered by the user
        :param password: Password entered by the user
        :return: UserAccount if a user was found, None otherwise
        """
        self.account = self.manager.get_account(username, password)
        return self.account

