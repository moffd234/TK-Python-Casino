import datetime
import re
import uuid

from Application.Model.Accounts.AccountManager import AccountManager
from Application.Model.Accounts.UserAccount import UserAccount


def is_password_valid(password: str) -> bool:
    """
    Checks if the password has the following requirements:
    - At least 8 characters long
    - At least one uppercase letter
    - At least one lowercase letter
    - At least one number
    - At least one special character

    :param password: password previously inputted by user
    :return: true if password is valid
    """
    pattern = r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[!@#$%^&*])[A-Za-z\d!@#$%^&*]{8,}$"
    return True if re.match(pattern, password) else False


def is_email_valid(email: str) -> bool:
    """
    Checks that the given email address has the following:
    - One or more character before an @ symbol
    - @ symbol
    - a . before a domain extension
    - Two or more characters for the domain extension after the .

    :param email: email previously inputted by user
    :return: return True if email is valid. Otherwise, returns False
    """
    pattern = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
    return True if re.match(pattern, email) else False


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

    def create_account(self, username: str, password: str, email: str,
                       security_questions: list[str]) -> tuple[bool, str | None]:
        """
        Attempts to create an account with the given credentials. Then returns True, None if successful.

        Validates email and username, then attempts to create an account with AccountManager.create_account. If
        successful returns True, None. Otherwise, returns False with an error message.
        :param username: Username entered by the user
        :param password: Password entered by the user
        :param email: Email entered by the user
        :param security_questions: A list containing the security questions and answers entered by the user
        :return: A tuple (success, error) where success is True if creation succeeded, and error is None or a message.
        """

        if is_email_valid(email) and is_password_valid(password):
            self.account = self.manager.create_account(username, password, email, security_questions)

        if not self.account:
            return False, "Account with that username already exists"

        return True, None

    def validate_email(self, email: str) -> UserAccount:
        """
        Attempts to find and return a user account associated with the given email.

        :param email: Email entered by the user.
        :return: The matching UserAccount if found, otherwise None.
        """
        self.account = self.manager.get_account_by_email(email)
        return self.account if self.account else None

    def email_reset_token(self) -> str:
        """
        Generates a reset token for the currently loaded account and sends it via email.

        Delegates token generation and email dispatch to AccountManager. Assumes that
        self.account has already been set via prior validation.

        :return: The generated reset token as a string.
        """
        self.manager.email_recovery_token(self.account)
        return self.account.reset_token

    def is_token_valid(self, token: str) -> bool:
        """
        Validates that the user's entered token matches the one stored and is not expired.

        :param token: The token entered by the user.
        :return: True if the token matches and has not expired, False otherwise.
        """
        try:
            input_token: uuid.UUID = uuid.UUID(token)
            now = datetime.datetime.now(datetime.UTC)
            expiration: datetime = self.account.reset_token_expiration.replace(tzinfo=datetime.timezone.utc)
            return self.account.reset_token == input_token and expiration >= now

        except ValueError:
            return False

    def reset_password(self, new_password) -> None:
        """
        Resets the password for the current UserAccount
        :param new_password: a new password entered by the user.
        :return: None
        """
        self.manager.update_password(self.account, new_password)