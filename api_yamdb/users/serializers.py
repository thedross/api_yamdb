from rest_framework import serializers

from users.models import CustomUser as User
from .mixins import ValidateUsernameMixin


class UserSerializer(serializers.ModelSerializer, ValidateUsernameMixin):
    """
    Сериализатор модели User.
    """
    class Meta:
        model = User
        fields = (
            'username',
            'email',
            'first_name',
            'last_name',
            'bio',
            'role'
        )


class CreateUserSerializer(serializers.ModelSerializer, ValidateUsernameMixin):
    """
    Сериализатор модели User для регистрации.
    """
    class Meta:
        model = User
        fields = ('username', 'email')

    def validate(self, data):
        """
        В случае полного совпадения емайл и юсернейма валидация пройдет,
        как раз на случай, если пользователь повторно запросит
        код подтверждения на почту.
        В случае частичного совпадения - нет.
        """
        username = data.get('username')
        email = data.get('email')

        if not User.objects.filter(username=username, email=email).exists():
            if (User.objects.filter(username=username).exists()
               or User.objects.filter(email=email).exists()):
                raise serializers.ValidationError(
                    'Пользователь с таким емайл или ником существует'
                )
        return data

    def create(self, validated_data):
        user, created = User.objects.get_or_create(**validated_data)

        if created:
            return user

        return validated_data


class TokenObtainSerializer(serializers.Serializer, ValidateUsernameMixin):
    """
    Сериализатор для получения токена.
    """
    user = serializers.SlugRelatedField(
        queryset=User.objects.all(),
        slug_field='username',
    )

    confirmation_code = serializers.CharField()
