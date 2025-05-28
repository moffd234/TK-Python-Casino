import unittest
from unittest.mock import patch, call

from Application.Utils.ANSI_COLORS import ANSI_COLORS
from Application.Utils.IOConsole import IOConsole, count_decimals
from Tests.BaseTest import IOCONSOLE_PATH


class TestIOConsole(unittest.TestCase):

    def setUp(self):
        self.console = IOConsole()

    def test_constructor_no_color(self):
        subject = IOConsole()
        self.assertEqual(subject.color, ANSI_COLORS.GREEN.value)

    def test_constructor_blue(self):
        subject = IOConsole(color=ANSI_COLORS.BLUE)
        self.assertEqual(subject.color, ANSI_COLORS.BLUE.value)

    def test_constructor_type_error(self):
        with self.assertRaises(TypeError):
            IOConsole(color="red")

    @patch("builtins.input", return_value="test input")
    def test_get_string_input(self, mock_input):
        subject = self.console.get_string_input("Some Prompt")
        self.assertEqual(subject, "test input")
        self.assertTrue(isinstance(subject, str))

    @patch("builtins.input", return_value="exit")
    def test_exit_called_with_code_0(self, mock_input):
        with self.assertRaises(SystemExit) as sys_exit:
            self.console.get_string_input("Some Prompt")

        self.assertEqual(sys_exit.exception.code, 0)

    @patch("builtins.print")
    @patch("builtins.input", return_value="test input")
    def test_get_string_input_default_color(self, mock_print, mock_input):
        self.console.get_string_input("Some Prompt")
        mock_print.assert_called_once_with(self.console.color + "Some Prompt\n")

    @patch("builtins.print")
    @patch("builtins.input", return_value="test input")
    def test_get_string_input_custom_color(self, mock_print, mock_input):
        self.console.get_string_input("Some Prompt", ANSI_COLORS.BLUE)
        mock_print.assert_called_once_with(ANSI_COLORS.BLUE.value + "Some Prompt\n")

    def test_check_for_exit_true(self):
        subject: bool = self.console.check_for_exit("exit")
        self.assertTrue(subject)

    def test_check_for_exit_false(self):
        subject: bool = self.console.check_for_exit("some input")
        self.assertFalse(subject)

    @patch("builtins.input", return_value="42")
    def test_get_integer_input_valid(self, mock_input):
        result = self.console.get_integer_input("Some prompt: ")
        self.assertEqual(result, 42)

    @patch("builtins.input", return_value="100")
    def test_get_integer_input_with_custom_color(self, mock_input):
        result = self.console.get_integer_input("Some prompt: ", ANSI_COLORS.BLUE)
        self.assertEqual(result, 100)

    @patch("builtins.input", side_effect=["####", "10"])
    @patch(f"{IOCONSOLE_PATH}.print_error")
    def test_get_integer_input_value_error(self, mock_print, mock_input):
        expected: int = 10
        actual: int = self.console.get_integer_input("Some prompt: ")

        mock_print.assert_called_once_with("#### is not a valid integer.")
        self.assertEqual(actual, expected)

    @patch("builtins.input", return_value="12")
    @patch(f"{IOCONSOLE_PATH}.is_in_range", return_value=True)
    def test_get_integer_input_valid_range_check(self, mock_range_change, mock_input):
        result = self.console.get_integer_input("Some prompt: ", range_vals=(10, 15))

        mock_range_change.assert_called_once_with(12, 10, 15)
        self.assertEqual(result, int(mock_input.return_value))

    @patch("builtins.input", side_effect=["12", "10"])
    @patch(f"{IOCONSOLE_PATH}.is_in_range", side_effect=[False, True])
    def test_get_integer_input_invalid_range_check(self, mock_range_change, mock_input):
        result = self.console.get_integer_input("Some prompt: ", range_vals=(10, 11))

        mock_range_change.assert_has_calls([call(12, 10, 11), call(10, 10, 11)])
        self.assertEqual(10, result)

    @patch("builtins.input", return_value="42.23")
    def test_get_float_input_valid(self, mock_input):
        result = self.console.get_float_input("Some prompt: ")
        self.assertEqual(result, 42.23)

    @patch("builtins.input", return_value="100.63")
    def test_get_float_input_with_custom_color(self, mock_input):
        result = self.console.get_float_input("Some prompt: ", ANSI_COLORS.BLUE)
        self.assertEqual(result, 100.63)

    @patch("builtins.input", side_effect=["####", "10.0"])
    @patch(f"{IOCONSOLE_PATH}.print_error")
    def test_get_float_input_value_error(self, mock_print, mock_input):
        expected: float = 10.0
        actual: float = self.console.get_float_input("Some prompt: ")

        mock_print.assert_called_once_with("#### is not a valid float.")
        self.assertEqual(actual, expected)

    @patch("builtins.input", return_value="12.56")
    @patch(f"{IOCONSOLE_PATH}.is_in_range", return_value=True)
    def test_get_float_input_valid_range_check(self, mock_range_change, mock_input):
        result = self.console.get_float_input("Some prompt: ", range_vals=(10.0, 15.3))

        mock_range_change.assert_called_once_with(12.56, 10.0, 15.3)
        self.assertEqual(result, float(mock_input.return_value))

    @patch("builtins.input", side_effect=["12.0", "10.0"])
    @patch(f"{IOCONSOLE_PATH}.is_in_range", side_effect=[False, True])
    def test_get_float_input_invalid_range_check(self, mock_range_change, mock_input):
        result = self.console.get_float_input("Some prompt: ", range_vals=(10.0, 11.0))

        mock_range_change.assert_has_calls([call(12.0, 10.0, 11.0), call(10.0, 10.0, 11.0)])
        self.assertEqual(10, result)

    @patch(f"{IOCONSOLE_PATH}.print_colored")
    def test_print_error(self, mock_print_colored):
        self.console.print_error("Some Prompt")
        mock_print_colored.assert_called_once_with("Some Prompt", ANSI_COLORS.RED)

    def test_count_decimals_0(self):
        expected: int = 0
        actual: int = count_decimals(123)

        self.assertEqual(expected, actual)

    def test_count_decimals_2(self):
        expected: int = 2
        actual: int = count_decimals(1.23)

        self.assertEqual(expected, actual)

    def test_count_decimals_5(self):
        expected: int = 5
        actual: int = count_decimals(1.23456)

        self.assertEqual(expected, actual)

    def test_count_decimals_end_in_0(self):
        expected: int = 1
        actual: int = count_decimals(1.1000000000000)

        self.assertEqual(expected, actual)

    @patch(f"{IOCONSOLE_PATH}.get_float_input", return_value=1.11)
    def test_get_monetary_input_valid_with_color(self, mock_input):
        expected: float = 1.11
        actual: float = self.console.get_monetary_input("Some Prompt", ANSI_COLORS.BLUE)

        mock_input.assert_called_once_with("Some Prompt", ANSI_COLORS.BLUE)
        self.assertEqual(expected, actual)

    @patch(f"{IOCONSOLE_PATH}.get_float_input", return_value=1.11)
    def test_get_monetary_input_valid_no_color(self, mock_input):
        expected: float = 1.11
        actual: float = self.console.get_monetary_input("Some Prompt")

        mock_input.assert_called_once_with("Some Prompt", None)
        self.assertEqual(expected, actual)

    @patch(f"{IOCONSOLE_PATH}.get_float_input", side_effect=[1.2345, 123.4])
    @patch(f"{IOCONSOLE_PATH}.print_error")
    def test_get_monetary_input_invalid_decimal_with_color(self, mock_print, mock_input):
        expected: float = 123.4
        actual: float = self.console.get_monetary_input("Some Prompt", ANSI_COLORS.BLUE)

        mock_input.assert_has_calls([
            call("Some Prompt", ANSI_COLORS.BLUE),
            call("Some Prompt", ANSI_COLORS.BLUE)
        ])
        mock_print.assert_called_once_with(
            "Please enter a valid amount (A positive number >= 1.00 with no more than 2 decimal places).")

        self.assertEqual(expected, actual)

    @patch(f"{IOCONSOLE_PATH}.get_float_input", side_effect=[1.2345, 123.4])
    @patch(f"{IOCONSOLE_PATH}.print_error")
    def test_get_monetary_input_invalid_decimal_no_color(self, mock_print, mock_input):
        expected: float = 123.4
        actual: float = self.console.get_monetary_input("Some Prompt")

        mock_input.assert_has_calls([
            call("Some Prompt", None),
            call("Some Prompt", None)
        ])
        mock_print.assert_called_once_with(
            "Please enter a valid amount (A positive number >= 1.00 with no more than 2 decimal places).")

        self.assertEqual(expected, actual)

    @patch(f"{IOCONSOLE_PATH}.get_float_input", side_effect=[0, 123.4])
    @patch(f"{IOCONSOLE_PATH}.print_error")
    def test_get_monetary_input_zero_with_color(self, mock_print, mock_input):
        expected: float = 123.4
        actual: float = self.console.get_monetary_input("Some Prompt", ANSI_COLORS.BLUE)

        mock_input.assert_has_calls([
            call("Some Prompt", ANSI_COLORS.BLUE),
            call("Some Prompt", ANSI_COLORS.BLUE)
        ])
        mock_print.assert_called_once_with(
            "Please enter a valid amount (A positive number >= 1.00 with no more than 2 decimal places).")

        self.assertEqual(expected, actual)

    @patch(f"{IOCONSOLE_PATH}.get_float_input", side_effect=[0, 123])
    @patch(f"{IOCONSOLE_PATH}.print_error")
    def test_get_monetary_input_zero_no_color(self, mock_print, mock_input):
        expected: float = 123
        actual: float = self.console.get_monetary_input("Some Prompt")

        mock_input.assert_has_calls([
            call("Some Prompt", None),
            call("Some Prompt", None)
        ])
        mock_print.assert_called_once_with(
            "Please enter a valid amount (A positive number >= 1.00 with no more than 2 decimal places).")

        self.assertEqual(expected, actual)

    @patch("builtins.input", return_value="y")
    def test_boolean_y(self, mock_input):
        actual: bool = self.console.get_boolean_input("Some Prompt")

        self.assertTrue(actual)

    @patch("builtins.input", return_value="yes")
    def test_boolean_yes(self, mock_input):
        actual: bool = self.console.get_boolean_input("Some Prompt")

        self.assertTrue(actual)

    @patch("builtins.input", return_value="true")
    def test_boolean_true(self, mock_input):
        actual: bool = self.console.get_boolean_input("Some Prompt")

        self.assertTrue(actual)

    @patch("builtins.input", return_value="1")
    def test_boolean_one(self, mock_input):
        actual: bool = self.console.get_boolean_input("Some Prompt")

        self.assertTrue(actual)

    @patch("builtins.input", return_value="TRUE")
    def test_boolean_true_cap(self, mock_input):
        actual: bool = self.console.get_boolean_input("Some Prompt")

        self.assertTrue(actual)

    @patch("builtins.input", return_value="n")
    def test_boolean_n(self, mock_input):
        actual: bool = self.console.get_boolean_input("Some Prompt")

        self.assertFalse(actual)

    @patch("builtins.input", return_value="no")
    def test_boolean_no(self, mock_input):
        actual: bool = self.console.get_boolean_input("Some Prompt")

        self.assertFalse(actual)

    @patch("builtins.input", return_value="false")
    def test_boolean_false(self, mock_input):
        actual: bool = self.console.get_boolean_input("Some Prompt")

        self.assertFalse(actual)

    @patch("builtins.input", return_value="0")
    def test_boolean_zero(self, mock_input):
        actual: bool = self.console.get_boolean_input("Some Prompt")

        self.assertFalse(actual)

    @patch("builtins.input", return_value="FALSE")
    def test_boolean_false_cap(self, mock_input):
        actual: bool = self.console.get_boolean_input("Some Prompt")

        self.assertFalse(actual)

    @patch("builtins.input", side_effect=["NotValidInput", "False"])
    @patch(f"{IOCONSOLE_PATH}.print_error")
    def test_boolean_invalid(self, mock_print, mock_input):
        actual: bool = self.console.get_boolean_input("Some Prompt")

        self.assertFalse(actual)

    @patch(f"{IOCONSOLE_PATH}.print_colored")
    def test_print_success(self, mock_print):
        self.console.print_success("Some Prompt")

        mock_print.assert_called_once_with("Some Prompt", ANSI_COLORS.GREEN)

    def test_is_in_range_true_int(self):
        actual: bool = self.console.is_in_range(15, 10, 20)
        self.assertTrue(actual)

    def test_is_in_range_false_int_too_large(self):
        actual: bool = self.console.is_in_range(15, 10, 11)
        self.assertFalse(actual)

    def test_is_in_range_false_int_too_small(self):
        actual: bool = self.console.is_in_range(15, 20, 21)
        self.assertFalse(actual)

    def test_is_in_range_true_float(self):
        actual: bool = self.console.is_in_range(15.0, 10.0, 20.0)
        self.assertTrue(actual)

    def test_is_in_range_false_float_too_small(self):
        actual: bool = self.console.is_in_range(15.0, 15.01, 20.0)
        self.assertFalse(actual)

    def test_is_in_range_false_float_too_large(self):
        actual: bool = self.console.is_in_range(15.0, 10.0, 14.99)
        self.assertFalse(actual)