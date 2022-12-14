from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.filters import SearchFilter
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from rest_framework_simplejwt.tokens import RefreshToken

from .models import User
from .permissions import IsAdmin
from .serializers import (UserAuthSerializer, UserSerializer,
                          UserTokenSerializer)


class UserViewSet(ModelViewSet):
    """Обработка запросов users/ users/<username>/ users/me/.
    CRUD всех users для админа через api-запросы. Профили для всех
    аутентифицированных пользователей с возможностью редактирования полей
    (кроме поля 'role').
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer
    lookup_field = 'username'
    permission_classes = (IsAdmin, )
    filter_backends = (SearchFilter,)
    search_fields = ('username',)

    @action(
        detail=False,
        methods=['get', 'patch'],
        permission_classes=[IsAuthenticated]
    )
    def me(self, request):
        if request.method == 'GET':
            serializer = UserSerializer(instance=request.user)
            return Response(
                serializer.data,
                status=status.HTTP_200_OK
            )
        serializer = UserSerializer(
            instance=request.user,
            data=request.data,
            partial=True
        )
        if serializer.is_valid():
            if not request.user.is_admin:
                if 'role' in serializer.validated_data:
                    serializer.validated_data['role'] = 'user'
            serializer.save()
            return Response(
                serializer.validated_data,
                status=status.HTTP_200_OK
            )
        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )


class UserAuthView(APIView):
    """Обработка запроса auth/signup/. Post запрос для создания
    пользователя через api. Получаем поля 'username', 'email'
    отправляем код подтверждения регистрации на почту."""
    permission_classes = (AllowAny,)

    def post(self, request):
        serializer = UserAuthSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(
            serializer.validated_data,
            status=status.HTTP_200_OK
        )


class UserTokenView(APIView):
    """Обработка запроса auth/token/. Post запрос для получения
    token для дальнейшей аутентификации. Получаем поля 'username',
    'confirmation_code' и если код валидный и не просрочен отправляем
    'token', 'срок жизни' токена ACCESS_TOKEN_LIFETIME в settings."""
    permission_classes = (AllowAny,)

    def post(self, request):
        serializer = UserTokenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = get_object_or_404(
            User,
            username=serializer.validated_data['username']
        )
        user.is_active = True
        user.save()
        token = RefreshToken.for_user(user)
        return Response(
            {'token': str(token.access_token)},
            status=status.HTTP_200_OK
        )
