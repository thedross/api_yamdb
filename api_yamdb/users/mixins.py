from users.validators import validate_username as validate


class ValidateUsernameMixin:
    def validate_username(self, username):
        return validate(username)
