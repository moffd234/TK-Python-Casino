import datetime
import uuid

from Application.Casino.Accounts.AccountManager import AccountManager, verify_password
from Application.Casino.Accounts.UserAccount import UserAccount
from Application.Casino.Games.CoinFlip.CoinFlip import CoinFlip
from Application.Casino.Games.NumberGuess.NumberGuess import NumberGuess
from Application.Casino.Games.RockPaperScissors.RPS import RPS
from Application.Casino.Games.Slots.Slots import Slots
from Application.Casino.Games.TicTacToe.TicTacToe import TicTacToe
from Application.Casino.Games.TriviaGame.TriviaGame import TriviaGame
from Application.Utils.ANSI_COLORS import ANSI_COLORS
from Application.Utils.IOConsole import IOConsole
import re


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


class Casino:
    def __init__(self):
        self.console = IOConsole(ANSI_COLORS.BLUE)
        self.manager = AccountManager()
        self.account: UserAccount | None = None

    def run(self) -> None:
        """
        Starts the casino application and transitions to menu screen
        :return: None
        """
        self.print_welcome()
        self.account: UserAccount = self.handle_initial_action()

        self.prompt_manage_or_select()

    def print_welcome(self) -> None:
        """
        Prints welcome message to the console
        :return: None
        """
        self.console.print_colored(r"""
            888       888          888                                         888 888 
            888   o   888          888                                         888 888 
            888  d8b  888          888                                         888 888 
            888 d888b 888  .d88b.  888  .d8888b .d88b.  88888b.d88b.   .d88b.  888 888 
            888d88888b888 d8P  Y8b 888 d88P"   d88""88b 888 "888 "88b d8P  Y8b 888 888 
            88888P Y88888 88888888 888 888     888  888 888  888  888 88888888 Y8P Y8P 
            8888P   Y8888 Y8b.     888 Y88b.   Y88..88P 888  888  888 Y8b.      "   "  
            888P     Y888  "Y8888  888  "Y8888P "Y88P"  888  888  888  "Y8888  888 888
            
            Notes:
                - At anypoint you can exit the application by typing "exit"
                - Funds can be added and you can reset you password from the manage account screen after logging in
            """)

    def handle_login(self) -> UserAccount | None:
        """
        Prompts the user to log in by entering their username and password.
        Allows up to 5 attempts before returning to the main screen.

        :return: UserAccount if credentials are valid, otherwise None.
        """
        for i in range(0, 5):

            username: str = self.console.get_string_input("Enter your username", return_in_lower=False)
            password: str = self.console.get_string_input("Enter your password", return_in_lower=False)

            account: UserAccount | None = self.manager.get_account(username=username, password=password)

            if account:
                return account
            else:
                self.console.print_error("Invalid username or password")

        self.console.print_error("Too many login attempts - returning to main screen\n\n\n")
        return None

    def handle_signup(self) -> UserAccount | None:
        """
        Guides the user through the sign-up process including entering a username, password, email,
        and answering two security questions. If the username already exists, the user is prompted to try again.

        :return: The created UserAccount, or None if the username is taken.
        """

        while True:
            username: str = self.prompt_username()
            password: str = self.prompt_password()
            email: str = self.prompt_email()
            security_questions: list[str] = self.get_security_questions_and_answers()

            account = self.manager.create_account(username, password, email, security_questions)

            if account:
                return account
            else:
                self.console.print_error("Account with that username already exists")

    def handle_initial_action(self) -> UserAccount:
        """
        Displays the main dashboard and prompts the user to either sign up, log in, or reset their password.
        Keeps prompting until a valid option is selected and a UserAccount is returned.

        :return: A valid UserAccount object after successful login or signup.
        """
        account: UserAccount | None = None

        while account is None:
            answer: str = self.console.get_string_input("Welcome to the Arcade Dashboard!" +
                                                        "\nFrom here, you can select any of the following options:" +
                                                        "\n\t[ signup ], [ login ], [ reset password ]")

            if answer == "login":
                account = self.handle_login()

            elif answer == "signup":
                account = self.handle_signup()

            elif answer == "reset" or answer == "reset password":
                self.reset_from_login()

            else:
                self.console.print_error("Invalid input. Please try again\n\n")

        return account

    def prompt_manage_or_select(self) -> None:
        """
        Prompts the user to either manage their account, select a game, or log out.
        If the user has insufficient funds, they are warned before attempting to select a game
        :return: None
        """
        while True:
            answer = self.console.get_string_input("You are logged in!" +
                                                   "\nFrom here, you can select any of the following options:" +
                                                   "\n\t[ manage-account ], [ select-game ], [ logout ]")

            if answer == "manage-account" or answer == "manage account" or answer == "manage":
                self.handle_manage_selection()

            elif answer == "select-game" or answer == "select game" or answer == "select":
                if self.account.balance < 1.00:
                    self.console.print_error("You do not have enough money to play any games")
                else:
                    self.prompt_game()
            elif answer == "logout":
                return None
            else:
                self.console.print_error("Invalid input. Please try again\n\n")

    def prompt_game(self) -> None:
        """
        Displays a list of available games and prompts the user to select one.
        Launches the selected game or returns to the previous menu if 'back' is entered.
        :return: None
        """
        while True:
            answer = self.console.get_string_input("Welcome to the Game Selection Dashboard!" +
                                                   "\nFrom here, you can select any of the following options:" +
                                                   "\n\t[ RPS ], [ NUMBERGUESS ], [ TRIVIA ], [ TIC-TAC-TOE ]. [ COINFLIP ], [ SLOTS ]")

            # The following are placeholders until the games are made
            if answer == "rps" or answer == "rock paper scissors":
                game = RPS(self.account, self.manager)
                game.run()

            elif answer == "numberguess" or answer == "number guess":
                game = NumberGuess(self.account, self.manager)
                game.run()

            elif answer == "trivia":
                game = TriviaGame(self.account, self.manager)
                game.run()

            elif answer == "tic-tac-toe" or answer == "tictactoe":
                game = TicTacToe(self.account, self.manager)
                game.run()

            elif answer == "coinflip" or answer == "coin flip":
                game = CoinFlip(self.account, self.manager)
                game.run()

            elif answer == "slots":
                game = Slots(self.account, self.manager)
                game.run()

            elif answer == "back":
                return None

            else:
                self.console.print_error("Invalid input. Please try again\n\n")

    def add_funds(self) -> None:
        """
        Prompts the user to enter an amount of money to add to their balance.
        Validates the input and updates the user's account with the new balance.
        :return: None
        """
        answer: float = self.console.get_monetary_input("Enter the amount of money you want to add to your funds"
                                                        " (no less than $1.00)")
        self.manager.add_and_save_account(self.account, answer)
        self.console.print_success(f"You have added ${answer} to your funds! New Balance is {self.account.balance}")

    def reset_password(self) -> bool:
        """
        Prompts the user to enter a new password and validates it.
        Allows up to 5 invalid attempts before aborting the update.

        :return: True if the password was successfully updated, False otherwise.
        """
        for _ in range(5):
            answer = self.console.get_string_input("Enter old password: ", return_in_lower=False)

            if verify_password(answer, self.account.password):
                was_successful: bool = self.update_password()
                return was_successful

            else:
                self.console.print_error("Passwords do not match")
        self.console.print_error("Too many invalid attempts. Please try again")
        return False

    def update_password(self) -> bool:
        """
        Prompts the user to enter a new password and validates it.
        Allows up to 5 invalid attempts before aborting the update.

        :return: True if the password was successfully updated, False otherwise.
        """
        password: str = self.console.get_string_input("Enter new password: ", return_in_lower=False)

        attempts_flag: int = 0
        while not is_password_valid(password) and attempts_flag < 5:
            self.console.print_error("Invalid password. Password must follow the following:\n"
                                     "- At least 8 characters long\n"
                                     "- At least one uppercase letter\n"
                                     "- At least one lowercase letter\n"
                                     "- At least one number\n"
                                     "- At least one special character")

            password = self.console.get_string_input("Enter new password: ", return_in_lower=False)
            attempts_flag += 1

        if attempts_flag != 5:
            self.manager.update_password(self.account, password)
            self.console.print_success(f"Your password has been updated!")
            return True

        else:
            self.console.print_error("Too many invalid attempts. Password was not updated.")
            return False

    def handle_manage_selection(self) -> None:
        """
        Prompts the user to choose an account management option: add funds, reset password, or go back.
        Executes the selected action.
        :return: None
        """
        while True:
            answer: str = self.console.get_string_input(f"You have ${self.account.balance}" +
                                                        "\nFrom here, you can select any of the following options:" +
                                                        "\n\t[ add-funds ], [reset-password], [ go-back ]")

            if answer == "add-funds" or answer == "add" or answer == "add funds":
                self.add_funds()
                return None

            elif answer == "reset-password" or answer == "reset" or answer == "reset password":
                self.reset_password()
                return None

            elif answer == "go-back" or answer == "go back" or answer == "back":
                return None

            else:
                self.console.print_error("Invalid input. Please try again")

    def get_security_question(self, possible_questions) -> str:
        """
        Displays a list of possible security questions and prompts the user to select one by number.

        :param possible_questions: A list of strings representing security questions.
        :return: The selected security question as a string.
        """
        self.console.print_colored("Please select a security question by typing the corresponding number: ")

        for i, question in enumerate(possible_questions):
            self.console.print_colored(f"{i}. {question}")

        answer: int = self.console.get_integer_input("Your choice: ", range_vals=(0, len(possible_questions) - 1))
        return possible_questions[answer]

    def get_security_questions_and_answers(self) -> list[str]:
        """
        Guides the user through selecting and answering two security questions.

        :return: A list containing two questions and their corresponding answers.
        """

        possible_questions: list[str] = [
            "What is your favorite sports team?",
            "What street did you grow up on?",
            "What was the name of your first pet?",
            "What is your mother’s maiden name?",
            "What was the name of your elementary school?",
            "In what city were you born?",
            "What was the make of your first car?",
            "What is your favorite movie?",
            "What is your childhood best friend's first name?",
            "What was the name of your first employer?",
            "What is your favorite food?",
            "What is the name of your favorite teacher?",
            "Where did you go on your first vacation?",
            "What is the middle name of your oldest sibling?",
            "What was the name of your first stuffed animal?"
        ]

        first_question: str = self.get_security_question(possible_questions)
        first_answer: str = self.console.get_string_input(f"You selected {first_question}. Please enter your answer")
        possible_questions.remove(first_question)

        second_question: str = self.get_security_question(possible_questions)
        second_answer: str = self.console.get_string_input(f"You selected {second_question}. Please enter your answer")

        return [first_question, first_answer, second_question, second_answer]

    def prompt_username(self) -> str | None:
        """
        Prompts the user to enter a username. If the user types "back", None is returned.

        :return: The username string or None.
        """
        username: str = self.console.get_string_input("Create your username or type back", return_in_lower=False)
        return None if username == "back" else username

    def prompt_password(self) -> str:
        """
        Prompts the user to enter a password and validates it using standard rules.
        Repeats the prompt until a valid password is provided.

        :return: The validated password string.
        """
        password: str = self.console.get_string_input("Create your password: ", return_in_lower=False)

        while not is_password_valid(password):
            self.console.print_error("Invalid password. Password must follow the following:\n"
                                     "- At least 8 characters long\n"
                                     "- At least one uppercase letter\n"
                                     "- At least one lowercase letter\n"
                                     "- At least one number\n"
                                     "- At least one special character")
            password = self.console.get_string_input("Enter new password: ", return_in_lower=False)

        return password

    def prompt_email(self) -> str:
        """
        Prompts the user to enter a valid email address. Repeats the prompt until the email format is valid.

        :return: The validated email string.
        """
        email: str = self.console.get_string_input("Enter your email: ", return_in_lower=False)

        while not is_email_valid(email):
            self.console.print_error("Invalid email.")
            email = self.console.get_string_input("Enter your email: ", return_in_lower=False)

        return email

    def validate_and_reset(self) -> bool:
        """
        Prompts the user to enter their password reset token and validates it.

        :return: True if the token is valid and the password was successfully updated, False otherwise.
        """
        for _ in range(5):
            user_input = self.console.get_string_input("Please enter your reset token sent to your email")

            if self.is_token_valid(user_input):
                was_success: bool = self.update_password()
                if was_success:
                    self.manager.invalidate_reset_token(self.account)
                return True

            self.console.print_error("Invalid or expired token. Please try again.")

        self.console.print_error("Too many attempts. Try again later.")
        return False

    def is_token_valid(self, user_input: str) -> bool:
        """
        Validates that the user's entered token matches the one stored and is not expired.

        :param user_input: The token entered by the user.
        :return: True if the token matches and has not expired, False otherwise.
        """
        try:
            input_token: uuid.UUID = uuid.UUID(user_input)
            now = datetime.datetime.now(datetime.UTC)
            expiration: datetime = self.account.reset_token_expiration.replace(tzinfo=datetime.timezone.utc)
            return self.account.reset_token == input_token and expiration >= now

        except ValueError:
            return False

    def prompt_and_check_email(self) -> bool:
        """
        Prompts user to enter the email associated with their account. Then searches if there is an account tied with
        that email address. User will have up to 5 attempts to do so, otherwise they will be prompted to try again later

        :return: True if the email is tied to an account, False otherwise.
        """
        for _ in range(5):

            email_input: str = self.console.get_string_input("Please enter the email associated with your account: ")

            self.account: UserAccount | None = self.manager.get_account_by_email(email_input)
            if self.account:
                return True
            else:
                self.console.print_error("Invalid email. Please try again.")

        self.console.print_error("Too many attempts. Try again later.")
        return False

    def prompt_for_security_answer(self, question: str, answer: str) -> bool:
        """
        Prompts the user to answer a provided security question with up to 5 attempts.

        :param question: The security question to display to the user.
        :param answer: The correct answer to validate against the user's input.
        :return: True if the answer is correct, False otherwise.
        """
        for _ in range(5):
            user_answer: str = self.console.get_string_input(question)
            if user_answer.strip() == answer.strip():

                return True
            else:
                self.console.print_error("Incorrect answer. Please try again.")

        self.console.print_error("Too many attempts. Try again later.")
        return False

    def get_security_answers(self) -> bool:
        """
        Sequentially prompts the user to answer two account security questions.

        :return: True if both security questions are correct, False otherwise.
        """
        if self.prompt_for_security_answer(self.account.security_question_one, self.account.security_answer_one):
            return self.prompt_for_security_answer(self.account.security_question_two, self.account.security_answer_two)

        return False

    def reset_from_login(self) -> bool:
        """
        Initiates the password reset process by verifying the user's identity.

        The user is prompted to enter their account email, followed by correct answers to their security questions.
        If both steps are successful, a reset token is emailed to the user, and they are prompted to enter it.
        Upon valid token entry, the user can set a new password.

        :return: True if the password was successfully reset, False otherwise.
        """
        if self.prompt_and_check_email() and self.get_security_answers():
            self.manager.email_recovery_token(self.account)
            return self.validate_and_reset()

        return False
