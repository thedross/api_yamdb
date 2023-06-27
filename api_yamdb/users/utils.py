from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail


def get_confirmation_code(user):
    """Генерирует код подтверждения."""
    return default_token_generator.make_token(user)


def send_email_comfirmation_code(user):
    """Отправляет письмо с кодом подтверждения на email."""
    send_mail(
        subject='Код подтверждения',
        message=f'Ваш код подтверждения: {get_confirmation_code(user)}',
        from_email=None,
        recipient_list=[user.email],
        fail_silently=False,
    )
