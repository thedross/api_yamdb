from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import default_token_generator
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import AccessToken

from rest_framework import filters, generics, viewsets, permissions

from users.serializers import (
    CreateUserSerializer,
    UserSerializer,
    TokenObtainSerializer
)
from users.utils import send_email_comfirmation_code

User = get_user_model()


class UsersViewSet(viewsets.ModelViewSet):
    """
    Вьюсет модели CustomUser.
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer
    filter_backends = (filters.SearchFilter, )
    search_fields = ('username', )


class CreateUserView(generics.GenericAPIView):
    """
    Вью для получения кода подтверждения.
    """
    queryset = User.objects.all()
    serializer_class = CreateUserSerializer
    permission_classes = (permissions.AllowAny, )

    def post(self, request, *args, **kwargs):
        # При самостоятельном создании пользователь сначала не активный
        serializer = CreateUserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(is_active=False)
            # Отправляем код подтверждения
            send_email_comfirmation_code(
                serializer.validated_data['email']
            )
            return Response(serializer.validated_data)
        # Вот здесь мы отправляем код без валидации поля email
        # Я не нашла очевидного способа обойти это
        send_email_comfirmation_code(serializer.data['email'])
        return Response(serializer.data)


class TokenObtainView(generics.GenericAPIView):
    """
    Вью для получения токена.
    """
    queryset = User.objects.all()
    serializer_class = TokenObtainSerializer
    permission_classes = (permissions.AllowAny, )

    def post(self, request, *args, **kwargs):
        user = User.objects.get(username=request.data['user'])
        confirmation_code = request.data['confirmation_code']
        # Токен генерируется на основе username насколько я понимаю,
        # поэтому нет необходимости его сохранять
        if default_token_generator.check_token(user, confirmation_code):
            user.is_active = True
            token = AccessToken.for_user(user)
            return Response(str(token))
        return Response("Неверный код подтверждения.")
