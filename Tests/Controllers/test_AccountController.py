import datetime
import uuid
from unittest.mock import patch

from Application.Controller.AccountController import AccountController, is_password_valid
from Application.Model.Accounts.AccountManager import AccountManager, verify_password
from Application.Model.Accounts.UserAccount import UserAccount
from Tests.BaseTest import ACCOUNT_MANAGER_CLASS_PATH, BaseTest, TEST_QUESTIONS


class TestAccountController(BaseTest):
    def setUp(self):
        super().setUp()
        manager = AccountManager()
        self.account_controller = AccountController(manager)
        test_account: UserAccount = UserAccount("test_username", "ValidPassword123!", 10.0,
                                                "email@testdomain.com", TEST_QUESTIONS)
        self.account_controller.account = test_account

    @patch(f"{ACCOUNT_MANAGER_CLASS_PATH}.get_account",
           return_value=UserAccount("test_username","ValidPassword123!",
                                    50.0, "test@email.com", TEST_QUESTIONS))
    def test_login_success(self, mock_get_account):
        actual: bool = self.account_controller.login("test_username", "ValidPassword123!")

        self.assertTrue(actual)
        self.assert_account_info(self.account_controller.account)
        mock_get_account.assert_called_once_with("test_username", "ValidPassword123!")

    def test_login_failure(self):
        actual: bool = self.account_controller.login("test_username", "InvalidPassword123!")
        self.assertFalse(actual)

    def test_is_password_valid_true(self):
        test_password: str = "validPassword123!"

        self.assertTrue(is_password_valid(test_password))

    def test_is_password_valid_exactly_8_chars(self):
        test_password: str = "validP1!"

        self.assertTrue(is_password_valid(test_password))

    def test_is_password_valid_too_short(self):
        test_password: str = "validPa"

        self.assertFalse(is_password_valid(test_password))

    def test_is_password_valid_no_uppercase(self):
        test_password: str = "valid_password123!"

        self.assertFalse(is_password_valid(test_password))

    def test_is_password_valid_no_lowercase(self):
        test_password: str = "VALID_PASSWORD123!"

        self.assertFalse(is_password_valid(test_password))

    def test_is_password_valid_only_letters(self):
        test_password: str = "vAlIdPaSsWoRd"

        self.assertFalse(is_password_valid(test_password))

    def test_is_password_valid_no_number(self):
        test_password: str = "validPassword!"

        self.assertFalse(is_password_valid(test_password))

    def test_is_password_only_number(self):
        test_password: str = "12345678"

        self.assertFalse(is_password_valid(test_password))

    def test_is_password_valid_no_special(self):
        test_password: str = "validPassword123"

        self.assertFalse(is_password_valid(test_password))

    def test_is_password_only_special(self):
        test_password: str = "!@#$%^&*("

        self.assertFalse(is_password_valid(test_password))

    def test_is_password_invalid_space_char(self):
        test_password: str = "ValidPassword  123!"

        self.assertFalse(is_password_valid(test_password))

    def test_is_password_invalid_tab_char(self):
        test_password: str = "ValidPassword\t123!"

        self.assertFalse(is_password_valid(test_password))

    def test_is_password_invalid_empty_string(self):
        test_password: str = ""

        self.assertFalse(is_password_valid(test_password))

    @patch(f"{ACCOUNT_MANAGER_CLASS_PATH}.get_account_by_email",
           return_value=UserAccount("test_username","ValidPassword123!",
                                    50.0, "test@email.com", TEST_QUESTIONS))
    def test_validate_email_true(self, mock_get_account):
        actual: UserAccount = self.account_controller.validate_email("test@email.com")

        self.assert_account_info(actual)
        mock_get_account.assert_called_once_with("test@email.com")

    @patch(f"{ACCOUNT_MANAGER_CLASS_PATH}.get_account_by_email",
           return_value=None)
    def test_validate_email_false(self, mock_get_account):
        actual: UserAccount = self.account_controller.validate_email("test@email.com")

        self.assertIsNone(actual)
        self.assertIsNone(self.account_controller.account)
        mock_get_account.assert_called_once_with("test@email.com")

    def test_is_token_valid_true(self):
        token: uuid.UUID = uuid.uuid4()
        self.account_controller.account.reset_token = token
        self.account_controller.account.reset_token_expiration = datetime.datetime.now(datetime.UTC) + datetime.timedelta(minutes=15)

        actual: bool = self.account_controller.is_token_valid(str(token))
        self.assertTrue(actual)

    def test_is_token_valid_incorrect_token(self):
        token: uuid.UUID = uuid.uuid4()
        self.account_controller.account.reset_token = uuid.uuid4()
        self.account_controller.account.reset_token_expiration = datetime.datetime.now(datetime.UTC) + datetime.timedelta(minutes=15)

        actual: bool = self.account_controller.is_token_valid(str(token))
        self.assertFalse(actual)

    def test_is_token_valid_not_uuid(self):
        token: str = "invalid token"
        self.account_controller.account.reset_token = uuid.uuid4()
        self.account_controller.account.reset_token_expiration = datetime.datetime.now(datetime.UTC) + datetime.timedelta(minutes=15)

        actual: bool = self.account_controller.is_token_valid(token)
        self.assertFalse(actual)

    def test_is_token_valid_expired(self):
        token: uuid.UUID = uuid.uuid4()
        self.account_controller.account.reset_token = token
        self.account_controller.account.reset_token_expiration = datetime.datetime.now(datetime.UTC) - datetime.timedelta(minutes=1)

        actual: bool = self.account_controller.is_token_valid(str(token))
        self.assertFalse(actual)

    def test_reset_password(self):
        self.account_controller.reset_password("NewValidPassword123!")
        actual: bool = verify_password("NewValidPassword123!", self.account_controller.account.password)

        self.assertTrue(actual)