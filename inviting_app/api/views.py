from time import sleep

from django.conf import settings
from django.contrib.auth import get_user_model
from django.db import transaction, IntegrityError
from django.shortcuts import get_object_or_404
from django.utils.crypto import get_random_string
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny, IsAdminUser, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import AccessToken

from profiles.models import Profile
from .serializers import (
    SignUpSerializer,
    AuthSerializer,
    ProfileSerializer
)

User = get_user_model()


class SignUpView(APIView):
    permission_classes = (AllowAny,)

    def post(self, request):
        serializer = SignUpSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        phone = serializer.validated_data['phone']
        self.check_or_create_profile(phone)
        code = self.send_code(phone)
        request.session['phone'] = phone
        request.session['code'] = code
        return Response({'code': code}, status=status.HTTP_200_OK)

    @staticmethod
    @transaction.atomic
    def check_or_create_profile(phone):
        try:
            user = User.objects.create_user(phone=phone)
            Profile.objects.create(
                user=user,
                invite_code=get_random_string(
                    settings.INVITE_CODE_LENGTH,
                    settings.RANDOM_CHARS
                )
            )
        except IntegrityError:
            return

    @staticmethod
    def send_code(phone):
        code = get_random_string(
            settings.AUTH_CODE_LENGTH,
            settings.RANDOM_CHARS
        )
        # Заглушка. Код должен отправляться на номер телефона
        sleep(2)
        return code


class AuthView(APIView):
    permission_classes = (AllowAny,)

    def post(self, request):
        serializer = AuthSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        code = serializer.validated_data['code']
        user = get_object_or_404(User, phone=request.session.get('phone'))
        if code != request.session.get('code'):
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST
            )
        token = AccessToken.for_user(user)
        return Response({'token': str(token)}, status=status.HTTP_200_OK)


class ProfileViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
    permission_classes = (IsAdminUser,)

    @action(
        methods=('get', 'post'),
        detail=False,
        permission_classes=(IsAuthenticated,)
    )
    def me(self, request):
        profile = request.user.profile
        if request.method == 'GET':
            serializer = ProfileSerializer(profile)
        else:
            serializer = ProfileSerializer(profile, data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.update(profile, serializer.validated_data)
        return Response(serializer.data, status=status.HTTP_200_OK)
