from rest_framework import serializers
from .base import CreateUserSerializer, DetailUserSerializer, UpdateUserSerializer
from apps.user.models import JuridicalUser


class JuridicalUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = JuridicalUser
        fields = ('company_name', 'bin', 'swift', 'kbe', 'iban', 'bank',
                  'post_address', 'official_address', 'position', 'user')


class CreateJuridicalUserSerializer(JuridicalUserSerializer):
    user = CreateUserSerializer(many=False)


class DetailJuridicalUserSerializer(JuridicalUserSerializer):
    user = DetailUserSerializer(many=False)


class UpdateJuridicalUserSerializer(JuridicalUserSerializer):
    user = UpdateUserSerializer(many=False)
