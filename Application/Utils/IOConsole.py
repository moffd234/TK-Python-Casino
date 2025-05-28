from Application.Utils.ANSI_COLORS import ANSI_COLORS


def count_decimals(num: float) -> int:
    """
    Counts the number of decimal places in a number and returns the value.

    :param num: The number to have its decimals counted.
    :return: The number of decimal digits
    """
    str_num = str(num)
    if '.' not in str_num:
        return 0
    return len(str_num.split('.')[1])


class IOConsole:
    """
    A utility class for managing user interaction with console using colorized output

    Attributes:
        color (str): The ANSI color code used for console prompts by default
    """
    def __init__(self, color:ANSI_COLORS=ANSI_COLORS.GREEN):
        if not isinstance(color, ANSI_COLORS):
            raise TypeError("color must be an instance of ANSI_COLORS")
        self.color:str = color.value

    def get_string_input(self, prompt: str, color:ANSI_COLORS=None, return_in_lower: bool=True) -> str:
        """
        Prompts the user for input via the console and returns their response.

        If color is specified the prompt will be printed using the given ANSI color.

        If user types 'exit' the application will exit.

        :param prompt: The prompt to be printed to the user
        :param color: Optional ANSI_COLOR to display the prompt in
        :param return_in_lower:  If True, converts and returns the input in lowercase
        :return: The user's input as a string
        """
        if color is None or not isinstance(color, ANSI_COLORS):
            color = self.color

        else:
            color = color.value

        user_input = input(color + prompt + "\n")
        if self.check_for_exit(user_input):
            exit(0)

        if return_in_lower:
            return user_input.lower()

        return user_input

    def get_integer_input(self, prompt: str, color:ANSI_COLORS=None, range_vals: tuple[int, int] = None) -> int:
        """
        Prompts the user to input an integer, optionally validating it against a specified range.

        :param prompt: The prompt to be displayed.
        :param color: Optional ANSI color to print the text in.
        :param range_vals: Optional (min, max) range that the input will be validated against.
        :return: A valid integer entered by the user.
        """
        while True:
            string_response: str = self.get_string_input(prompt, color)
            try:
                input_num: int = int(string_response)

                if range_vals is None:
                    return input_num
                elif self.is_in_range(input_num, range_vals[0], range_vals[1]):
                    return input_num

            except ValueError:
                self.print_error(f"{string_response} is not a valid integer.")

    def get_float_input(self, prompt: str, color: ANSI_COLORS=None, range_vals: tuple[float, float] = None) -> float:
        """
        Prompts the user to input a float, optionally validating it against a specified range.

        :param prompt: The prompt to be displayed.
        :param color: Optional ANSI color to print the text in.
        :param range_vals: Optional (min, max) range that the input will be validated against.
        :return: A valid float entered by the user.
        """
        while True:
            string_response: str = self.get_string_input(prompt, color)
            try:
                input_num: float = float(string_response)

                if range_vals is None:
                    return input_num
                elif self.is_in_range(input_num, range_vals[0], range_vals[1]):
                    return input_num
            except ValueError:
                self.print_error(f"{string_response} is not a valid float.")

    def get_boolean_input(self, prompt: str, color: ANSI_COLORS = None) -> bool:
        """
        Prompts the user to input a boolean then returns it.

        :param prompt: The prompt to be displayed.
        :param color: Optional ANSI color to print the text in.
        :return: A valid boolean entered by the user.
        """
        while True:
            string_response: str = self.get_string_input(prompt, color)
            string_response = string_response.strip().lower()

            if string_response in ["yes", "y", "true", "1"]:
                return True
            elif string_response in ["no", "n", "false", "0"]:
                return False
            else:
                self.print_error(f"{string_response} is not a valid boolean. Please enter yes or no.")

    def check_for_exit(self, user_input: str) -> bool:
        """
        Checks if the user input is the command to exit the application.

        If the user types "exit", a message is printed and True is returned. Otherwise, returns False.

        :param user_input: The string input provided by the user.
        :return: True if the input is "exit", False otherwise.
        """

        if user_input.lower() == "exit":
            print(self.color + "Exiting the game")
            return True
        return False

    def print_colored(self, prompt: str, color: ANSI_COLORS = None) -> None:
        """
        Prints the provided prompt text in the specified ANSI color.

        If no color is provided or the provided color is invalid, the default color is used.

        :param prompt: The text to be printed to the console.
        :param color: Optional ANSI_COLORS value to style the output text.
        """

        if color is None or not isinstance(color, ANSI_COLORS):
            color = self.color

        else:
            color = color.value

        print(color + prompt)

    def print_error(self, error_message: str) -> None:
        """
        Takes an error message and prints it in ANSI_COLORS.RED.
        :param error_message: A string value that will be printed as the error message
        :return: None
        """
        self.print_colored(error_message, ANSI_COLORS.RED)

    def get_monetary_input(self, prompt, color: ANSI_COLORS=None) -> float:
        """
        Prompts the user to enter a monetary amount and validates the input.
        The user will be re-prompted until a valid positive number  >= 1.00 with no more than two decimal places is entered.

        :param prompt: A string value that will be printed as the prompt
        :param color: A color from ANSI_COLORS which will be used as the printed color
        :return: A valid monetary input float
        """
        money_input: float = self.get_float_input(prompt, color)

        while count_decimals(money_input) > 2 or money_input < 1.00:
            self.print_error("Please enter a valid amount "
                             "(A positive number >= 1.00 with no more than 2 decimal places).")
            money_input = self.get_float_input(prompt, color)

        return money_input

    def print_success(self, message: str) -> None:
        """
        Prints a success message in green.
        :param message: Message to print.
        :return: None
        """
        self.print_colored(message, ANSI_COLORS.GREEN)

    def is_in_range(self, user_input: int | float, min_val: int | float, max_val: int | float) -> bool:
        """
        Checks if provided user input falls within a given range. If so, the method returns True.
         Otherwise, returns False.
        :param user_input: The value to be checked if it is within range
        :param min_val: Minimum allowable value
        :param max_val: Maximum allowable value
        :return: True if user_input is within range, False otherwise
        """
        if not (min_val <= user_input <= max_val):
            self.print_error(f"{user_input} is out of range. "
                             f"Please enter a value between {min_val} and {max_val}.")
            return False
        return True