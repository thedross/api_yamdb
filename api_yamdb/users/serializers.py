from rest_framework import serializers

from users.models import CustomUser as User
from users.mixins import ValidateUsernameMixin


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
        extra_kwargs = {
            'username': {
                'validators': []
            },
            'email': {
                'validators': []
            }
        }

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
            if User.objects.filter(username=username).exists():
                raise serializers.ValidationError(
                    {'username': 'Пользователь с таким ником уже существует'}
                )
            if User.objects.filter(email=email).exists():
                raise serializers.ValidationError(
                    {'email': 'Пользователь с таким email уже существует'}
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
        label='Ник',
        queryset=User.objects.all(),
        slug_field='username',
    )

    confirmation_code = serializers.CharField(
        label='Код подтверждения'
    )
