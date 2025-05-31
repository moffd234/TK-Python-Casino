import unittest
from unittest.mock import patch

from Application.Controller.AccountController import AccountController
from Application.Model.Accounts.AccountManager import AccountManager
from Application.Model.Accounts.UserAccount import UserAccount
from Tests.BaseTest import ACCOUNT_MANAGER_CLASS_PATH, BaseTest, TEST_QUESTIONS


class TestAccountController(BaseTest):
    def setUp(self):
        super().setUp()
        manager = AccountManager()
        self.account_controller = AccountController(manager)
        test_account: UserAccount = UserAccount("test_username", "ValidPassword123!", 10.0,
                                                "email@testdomain.com", TEST_QUESTIONS)

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