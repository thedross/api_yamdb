import re

from django.core.exceptions import ValidationError


def validate_username(username):
    """
    Валидатор для username.
    Если username НЕ соответствует шаблону, то re.sub вернет True.
    В случае соответствия шаблону re.sub вернет пустую строку, т.е. False.
    """
    if (re.sub(r'^[\w.@+-]+$', '', username)
       or username.lower() == 'me'):
        raise ValidationError(
            f'Ошибка при проверке "{username}" \n'
            'для имени пользователя можно использовать'
            ' только буквы, цифры и символы _ . @ + - \n'
            'Нельзя использовать "me".'
        )
    else:
        return username
