from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import default_token_generator
from rest_framework import (
    status,
    filters,
    generics,
    viewsets,
    permissions,
)
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import AccessToken

from users.serializers import (
    CreateUserSerializer,
    GetCodeSerializer,
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
    serializer_class = GetCodeSerializer
    permission_classes = (permissions.AllowAny, )

    def post(self, request, *args, **kwargs):
        serializer_get = GetCodeSerializer(data=request.data)
        if serializer_get.is_valid(raise_exception=True):
            try:
                user = User.objects.get(
                    email=serializer_get.validated_data.get('email')
                )
                if user.username != serializer_get.validated_data.get('username'):
                    return Response(
                        serializer_get.validated_data,
                        status=status.HTTP_400_BAD_REQUEST
                    )
            except ObjectDoesNotExist:
                serializer_create = CreateUserSerializer(data=request.data)
                if serializer_create.is_valid():
                    serializer_create.save(is_active=False)
                    send_email_comfirmation_code(
                        serializer_create.validated_data.get('email')
                    )
                    return Response(
                        serializer_create.validated_data,
                        status=status.HTTP_200_OK
                    )
        try:
            send_email_comfirmation_code(
                serializer_get.validated_data.get('email')
            )
        except ObjectDoesNotExist:
            return Response(
                serializer_create.validated_data,
                status=status.HTTP_400_BAD_REQUEST
            )
        return Response(
            serializer_get.validated_data,
            status=status.HTTP_200_OK
        )


class TokenObtainView(generics.GenericAPIView):
    """
    Вью для получения токена.
    """
    queryset = User.objects.all()
    serializer_class = TokenObtainSerializer
    permission_classes = (permissions.AllowAny, )

    def post(self, request, *args, **kwargs):
        if not request.data.get('username'):
            return Response(status=status.HTTP_400_BAD_REQUEST)
        try:
            user = User.objects.get(username=request.data.get('username'))
        except ObjectDoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        confirmation_code = request.data.get('confirmation_code')
        if default_token_generator.check_token(user, confirmation_code):
            user.is_active = True
            token = AccessToken.for_user(user)
            return Response(str(token))
        return Response(
            "Неверный код подтверждения.",
            status=status.HTTP_400_BAD_REQUEST
        )
