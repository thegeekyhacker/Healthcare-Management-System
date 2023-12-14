import re

def is_valid_password(password):
    if len(password) != 10:
        return False
    if not any(c.islower() for c in password):
        return False
    if not any(c.isupper() for c in password):
        return False
    if not any(c.isdigit() for c in password):
        return False
    if not re.search(r'[!@#$%^&*?]', password):
        return False
    return True

