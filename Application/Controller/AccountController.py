from Application.Model.Accounts.AccountManager import AccountManager
from Application.Model.Accounts.UserAccount import UserAccount


class AccountController:
    def __init__(self, manager: AccountManager):

        self.manager: AccountManager = manager
        self.account: UserAccount | None = None

    def login(self, username: str, password: str) -> bool:
        """
        Attempts to authenticate a user with the given credentials

        If user account that matches the username and password exists,
        self.account is set to the account and True is returned.
        Otherwise, False is returned.

        :param username: Username entered by the user
        :param password: Password entered by the user
        :return: True if a user was found, False otherwise
        """
        self.account = self.manager.get_account(username, password)
        return self.account is not None

