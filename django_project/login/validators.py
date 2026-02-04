import re
from django.core.exceptions import ValidationError

class custom_password_validator:
    def validate(self, password, username=None):
        errors = []

        if len(password) < 8:
            errors.append("password should be at least 8 characters long.")

        if not re.search(r"[A-Z]", password):
            errors.append("password should contain at least one uppercase letter.")

        if not re.search(r"[a-z]", password):
            errors.append("password should contain at least one lowercase letter.")

        if not re.search(r"\d", password):
            errors.append("password should contain at least one digit.")

        if not re.search(r"[!@#$%^&*(),.?\":{}|<>]", password):
            errors.append("password should contain at least one special character.")

        if username and username.username.lower() in password.lower():
            errors.append("Password should not contain the username.")

        if errors:
            raise ValidationError(errors)
