from django.core.mail import send_mail
from django.contrib.auth.tokens import default_token_generator

from users.models import CustomUser as User


def get_confirmation_code(email):
    """Генерирует код подтверждения."""
    return default_token_generator.make_token(User.objects.get(email=email))


def send_email_comfirmation_code(email):
    """Отправляет письмо с кодом подтверждения на email."""
    send_mail(
        subject='Код подтверждения',
        message=f'Ваш код подтверждения: {get_confirmation_code(email)}',
        from_email=None,
        recipient_list=[email],
        fail_silently=False,
    )
