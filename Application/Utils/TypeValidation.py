def validate_float(user_input: str):
    try:
        float(user_input)
        return True
    except ValueError:
        return False
