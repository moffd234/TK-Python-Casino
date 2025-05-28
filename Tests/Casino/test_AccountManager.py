import datetime
import uuid
from unittest.mock import MagicMock, patch

from Application.Casino.Accounts.AccountManager import hash_password, verify_password
from Tests.BaseTest import BaseTest, TEST_QUESTIONS
from Application.Casino.Accounts.UserAccount import UserAccount


class TestAccountManager(BaseTest):

    def setUp(self):
        super().setUp()

    def test_create_account(self):
        subject = self.manager.create_account("username", "password", "test@email.com", TEST_QUESTIONS)

        expected_username: str = "username"
        expected_password: str = "password"
        expected_balance: float = 50.0

        actual_username: str = subject.username
        is_password_correct: bool = verify_password(expected_password, subject.password)
        actual_balance: float = subject.balance

        self.assertEqual(expected_username, actual_username)
        self.assertTrue(is_password_correct)
        self.assertEqual(expected_balance, actual_balance)

    def test_create_account_username_exist(self):
        self.manager.create_account("test_username", "test_password", "test@email.com", TEST_QUESTIONS)
        subject = self.manager.create_account("test_username", "test_password", "test@email.com", TEST_QUESTIONS)

        self.assertIsNone(subject)

    def assert_account_info(self, actual: UserAccount, hashed_password: str | None = None):
        expected = UserAccount("test_username", "test_password", 50.0,
                               "test@email.com", TEST_QUESTIONS)

        self.assertEqual(expected.username, actual.username)
        self.assertEqual(expected.balance, actual.balance)
        self.assertEqual(expected.email, actual.email)
        self.assertEqual(expected.security_question_one, actual.security_question_one)
        self.assertEqual(expected.security_question_two, actual.security_question_two)
        self.assertEqual(expected.security_answer_one, actual.security_answer_one)
        self.assertEqual(expected.security_answer_two, actual.security_answer_two)

        if hashed_password:
            verify_password("test_password", hashed_password)
        else:
            self.assertEqual(expected.password, actual.password)

    def test_get_account(self):
        self.manager.create_account("test_username", "test_password",
                                    "test@email.com", TEST_QUESTIONS)
        actual = self.manager.get_account("test_username", "test_password")
        self.assert_account_info(actual, hashed_password=actual.password)


    def test_get_account_none(self):
        actual: UserAccount = self.manager.get_account("this_name_won't_be_used", "secure123")

        self.assertIsNone(actual)

    def test_add_winnings_and_save(self):
        account: UserAccount = self.manager.create_account("test_username", "test_password",
                                                           "test@email.com", TEST_QUESTIONS)
        self.manager.session.commit = MagicMock()
        self.manager.add_and_save_account(account, 50.0)

        expected: float = 100
        actual: float = account.balance

        self.assertEqual(expected, actual)
        self.manager.session.commit.assert_called_once()

    def test_subtract_and_save(self):
        account: UserAccount = self.manager.create_account("test_username", "test_password",
                                                           "test@email.com", TEST_QUESTIONS)
        self.manager.session.commit = MagicMock()
        self.manager.subtract_and_save_account(account, 50.0)

        expected: float = 0
        actual: float = account.balance

        self.assertEqual(expected, actual)
        self.manager.session.commit.assert_called_once()

    @patch("sqlalchemy.orm.Session.commit")
    def test_generate_uuid(self, mock_commit):
        current_time: datetime = datetime.datetime.now(datetime.UTC)
        min_time: datetime = current_time + datetime.timedelta(minutes=14, seconds=59)
        max_time: datetime = current_time + datetime.timedelta(minutes=15, seconds=1)

        expected_token: uuid.UUID = uuid.UUID(self.manager.generate_uuid_and_store_it(self.account))
        actual_token: uuid.UUID = self.account.reset_token
        actual_expiration = self.account.reset_token_expiration

        is_time_valid: bool = min_time < actual_expiration < max_time

        mock_commit.assert_called_once()
        self.assertEqual(expected_token, actual_token)
        self.assertTrue(is_time_valid)

    def test_invalidate_reset_token(self):
        self.account.reset_token = uuid.uuid4()
        self.account.reset_token_expiration = datetime.datetime.now()

        self.manager.invalidate_reset_token(self.account)

        self.assertIsNone(self.account.reset_token)
        self.assertIsNone(self.account.reset_token_expiration)

    def test_get_account_by_email(self):
        self.manager.create_account("test_username", "test_password",
                                    "test@email.com", TEST_QUESTIONS)
        actual_account: UserAccount = self.manager.get_account_by_email("test@email.com")

        self.assert_account_info(actual_account, hashed_password=actual_account.password)

    def test_get_account_by_email_fail(self):
        account: UserAccount = self.manager.get_account_by_email("WRONG_EMAIL@DOMAIN.com")
        self.assertIsNone(account)

    def test_hash_password(self):
        password: str = "ValidPassword123!"
        hashed_password: str = hash_password(password)

        self.assertNotEqual(password, hashed_password)

    def test_hash_passwords_dont_match(self):
        password: str = "ValidPassword123!"
        hashed_password_one: str = hash_password(password)
        hashed_password_two: str = hash_password(password)

        self.assertNotEqual(hashed_password_one, hashed_password_two)

    @patch("bcrypt.gensalt", return_value=b"salt")
    @patch("bcrypt.hashpw", return_value=b"hashed_password")
    def test_hash_passwords_assert_calls(self, mock_hashpw, mock_gensalt):
        expected: str = "hashed_password"
        actual: str = hash_password("Password")

        mock_hashpw.assert_called_once_with(b"Password", mock_gensalt.return_value)
        mock_gensalt.assert_called_once()
        self.assertEqual(expected, actual)

    def test_verify_password_true(self):
        password: str = "ValidPassword123!"
        hashed_password: str = hash_password(password)

        actual: bool = verify_password(password, hashed_password)
        self.assertTrue(actual)

    def test_verify_password_false(self):
        password: str = "ValidPassword123!"
        hashed_password: str = hash_password(password)

        actual: bool = verify_password("password", hashed_password)
        self.assertFalse(actual)

    def test_verify_password_empty_string(self):
        password: str = "ValidPassword123!"
        hashed_password: str = hash_password(password)

        actual: bool = verify_password("", hashed_password)
        self.assertFalse(actual)