from django.db import transaction
from rest_framework import serializers
from djoser.serializers import UserSerializer, UserCreateSerializer
from djoser.conf import settings
from django.contrib.auth import get_user_model

User = get_user_model()


class SimpleUserSerializer(UserSerializer):
    class Meta:
        model = User
        fields = tuple(User.REQUIRED_FIELDS) + (
            'email',
            'is_admin'
        )


class DetailUserSerializer(UserSerializer):
    class Meta:
        model = User
        fields = tuple(User.REQUIRED_FIELDS) + (
            'id',
            'email',
            'balance',
            'spent_balance',
            'is_admin'
        )


class CreateUserSerializer(UserCreateSerializer):
    is_active = serializers.HiddenField(default=False)

    class Meta:
        model = User
        fields = tuple(User.REQUIRED_FIELDS) + (
            settings.LOGIN_FIELD,
            settings.USER_ID_FIELD,
            "password",
            "is_active"
        )


class UpdateUserSerializer(DetailUserSerializer):
    class Meta:
        model = User
        fields = tuple(User.REQUIRED_FIELDS) + (
            settings.LOGIN_FIELD,
            settings.USER_ID_FIELD,
            "password"
        )


class VerificationCodeSerializer(serializers.Serializer):
    code = serializers.CharField(min_length=8, max_length=8)


class ResetPasswordSerializer(serializers.Serializer):
    email = serializers.EmailField()
