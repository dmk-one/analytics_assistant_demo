from django.contrib.auth.models import update_last_login
from rest_framework.exceptions import AuthenticationFailed
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer, login_rule, user_eligible_for_login
from rest_framework_simplejwt.settings import api_settings

from apps.user.exceptions import UserNotActive, UserNotFound, UserCredentialsError
from apps.user.models import User


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        email = attrs['email']

        is_active = True

        try:
            is_active = User.objects.filter(email=email).first().is_active
        except AttributeError as e:
            raise UserNotFound

        if is_active is False:
            raise UserNotActive

        try:
            data = super().validate(attrs)
        except AuthenticationFailed as e:
            raise UserCredentialsError

        refresh = self.get_token(self.user)

        data['refresh'] = str(refresh)
        data['access'] = str(refresh.access_token)
        data['is_admin'] = self.user.is_admin

        if api_settings.UPDATE_LAST_LOGIN:
            update_last_login(None, self.user)

        return data
