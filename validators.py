def validate_days(days: int):
    if days < 1 or days > 10:
        raise ValueError("Days must be between 1 and 10.")
