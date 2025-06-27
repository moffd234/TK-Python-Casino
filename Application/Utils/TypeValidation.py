def validate_float(user_input: str, min_value=1.00):
    """
    Validates that the given input string represents a float greater than a minimum value.

    :param user_input: String inputted by user
    :param min_value: The minimum acceptable float value. Defaults to 1.00.
    :return: True if the input is a valid float greater than min_value, or if no minimum is specified. False if the
             input is not a valid float or does not meet the minimum requirement.
    """
    try:
        float_val: float = float(user_input)
        if min_value:
            return float_val > min_value
        return True

    except ValueError:
        return False
