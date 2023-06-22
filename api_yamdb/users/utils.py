from django.core.mail import send_mail
from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import default_token_generator

User = get_user_model()


def get_confirmation_code(email):
    """Генерирует код подтверждения."""
    return default_token_generator.make_token(User.objects.get(email=email))


def send_email_comfirmation_code(email):
    """Отправляет письмо с кодом подтверждения на email."""
    send_mail(
        'Код подтверждения',
        f'Ваш код подтверждения: {get_confirmation_code(email)}',
        'YaMDB',
        [email],
        fail_silently=False
    )
