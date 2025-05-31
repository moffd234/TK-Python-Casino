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
