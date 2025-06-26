def validate_float(user_input: str, min_value=None):
    try:
        float_val: float = float(user_input)
        if min_value:
            return float_val > min_value
        return True

    except ValueError:
        return False
