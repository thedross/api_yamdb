from django.contrib.auth import get_user_model

from rest_framework import serializers

# from users.validators import

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
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


class CreateUserSerializer(serializers.ModelSerializer):
    """
    Сериализатор модели User для регистрации.
    """
    class Meta:
        model = User
        fields = ('username', 'email')


class TokenObtainSerializer(serializers.Serializer):
    """
    Сериализатор для получения токена.
    """
    user = serializers.SlugRelatedField(
        queryset=User.objects.all(),
        slug_field='username'
    )

    confirmation_code = serializers.CharField()

    def validate_user(self, value):
        return value
