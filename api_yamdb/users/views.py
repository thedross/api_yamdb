from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import default_token_generator
from rest_framework import (
    filters,
    generics,
    permissions,
    status,
    viewsets,
)
from django.shortcuts import get_object_or_404
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import AccessToken

from api.permissions import (
    IsSuperOrAdmin
)
from users.serializers import (
    CreateUserSerializer,
    GetCodeSerializer,
    TokenObtainSerializer,
    UserSerializer,
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
        User = get_user_model()
        self.object = get_object_or_404(User, pk=request.user.id)
        if request.method == 'GET':
            serializer = self.get_serializer(self.object)
            return Response(serializer.data)
        serializer = self.get_serializer(data=request.data, partial=True)
        serializer.instance = self.object
        serializer.is_valid(raise_exception=True)
        serializer.save(
            instance=self.object,
            role=self.object.role
        )
        return Response(serializer.validated_data)


class CreateUserView(generics.GenericAPIView):
    """
    Вью для получения кода подтверждения.
    """
    queryset = User.objects.all()
    serializer_class = GetCodeSerializer
    permission_classes = (permissions.AllowAny, )

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            user = User.objects.get(
                email=serializer.validated_data.get('email')
            )
            if user.username != serializer.validated_data.get('username'):
                return Response(
                    serializer.validated_data,
                    status=status.HTTP_400_BAD_REQUEST
                )
        except ObjectDoesNotExist:
            serializer = CreateUserSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save(is_active=False)
        try:
            send_email_comfirmation_code(
                serializer.validated_data.get('email')
            )
        except ObjectDoesNotExist:
            return Response(
                serializer.validated_data,
                status=status.HTTP_400_BAD_REQUEST
            )
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
            return Response(
                str(token),
                status=status.HTTP_200_OK
            )
        return Response(
            "Неверный код подтверждения.",
            status=status.HTTP_400_BAD_REQUEST
        )
