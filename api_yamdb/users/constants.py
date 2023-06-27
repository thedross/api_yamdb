"""
Contstants used in:
- users.models
"""

USER = 'user'
MODERATOR = 'moderator'
ADMIN = 'admin'
CHOICES_ROLE = [
    (USER, 'Пользователь'),
    (MODERATOR, 'Модератор'),
    (ADMIN, 'Админ')
]

MAX_NAME_LENGTH = 150
MAX_EMAIL_LENGTH = 254
