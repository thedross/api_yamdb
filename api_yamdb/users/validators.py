import re

from django.core.exceptions import ValidationError

STRING_USERNAME = r'^[\w.@+-]+$'


def validate_username(username):
    """
    Валидатор для username.
    Если username НЕ соответствует шаблону, то re.sub вернет True.
    В случае соответствия шаблону re.sub вернет пустую строку, т.е. False.
    """
    resub_username = re.sub(STRING_USERNAME, '', ''.join(set(username)))

    if resub_username:
        raise ValidationError(
            f'Ошибка при проверке "{username}" \n'
            f'введены запрещенные символы: {resub_username}'
            'для имени пользователя можно использовать'
            ' только буквы, цифры и символы _ . @ + - \n'
        )
    if username.lower() == 'me':
        return 'Нельзя использовать "me".'
    return username
