from django.contrib.auth.tokens import default_token_generator
from django.shortcuts import get_object_or_404
from rest_framework import (
    filters,
    generics,
    permissions,
    status,
    viewsets,
)
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import AccessToken

from api.permissions import IsSuperOrAdmin
from users.models import CustomUser as User
from users.serializers import (
    CreateUserSerializer,
    TokenObtainSerializer,
    UserSerializer,
)
from users.utils import send_email_comfirmation_code


class UsersViewSet(viewsets.ModelViewSet):
    """
    Вьюсет модели CustomUser.
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer
    filter_backends = (filters.SearchFilter, )
    search_fields = ('username', )
    permission_classes = (
        permissions.IsAuthenticated,
        IsSuperOrAdmin
    )
    lookup_field = "username"
    http_method_names = ['get', 'post', 'head', 'patch', 'delete']

    @action(
        detail=False,
        methods=['get', 'head', 'patch'],
        permission_classes=(permissions.IsAuthenticated, )
    )
    def me(self, request, *args, **kwargs):
        current_user = User.objects.get(pk=request.user.id)
        if request.method == 'GET':
            return Response(UserSerializer(current_user).data)
        serializer = self.get_serializer(data=request.data, partial=True)
        serializer.instance = current_user
        serializer.is_valid(raise_exception=True)
        serializer.save(
            instance=current_user,
            role=current_user.role
        )
        return Response(serializer.validated_data)


class CreateUserView(generics.GenericAPIView):
    """
    Вью для получения кода подтверждения.
    """
    queryset = User.objects.all()
    serializer_class = CreateUserSerializer
    permission_classes = (permissions.AllowAny, )

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        user = User.objects.get(email=serializer.validated_data.get('email'))
        send_email_comfirmation_code(user)
        return Response(
            serializer.validated_data,
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
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = get_object_or_404(
            User, username=serializer.validated_data.get('username')
        )
        if default_token_generator.check_token(
            user=user,
            token=request.data.get('confirmation_code')
        ):
            user.is_active = True
            user.save()
            return Response(
                f'Your token: {str(AccessToken.for_user(user))}',
                status=status.HTTP_200_OK
            )
        return Response(
            {'confirmation_code': 'Неверный код подтверждения.'},
            status=status.HTTP_400_BAD_REQUEST
        )
