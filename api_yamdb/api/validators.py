from django.core.exceptions import ValidationError


def validate(value):
    if value.lower() == 'me':
        raise ValidationError('Значение "me" недопустимо')