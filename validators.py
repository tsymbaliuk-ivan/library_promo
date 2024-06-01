from django.core.exceptions import ValidationError
from re import match


def validate_password(password: str):
    if not match(r"^(?=.*[A-Z])(?=.*[a-z])(?=.*\d)(?=.*[@#$!%*?&])[A-Za-z\d@#$!%*?&]{8,}$", password):
        raise ValidationError("Try another password")

    else:
        return password

def validate_names(data: str):
    if not (data[0].isupper() and data.isalpha()):
        raise ValidationError("First letter must be uppercase, use only letters")
    else:
        return data