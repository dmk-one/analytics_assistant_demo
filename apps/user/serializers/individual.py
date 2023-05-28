from rest_framework import serializers
from .base import CreateUserSerializer, DetailUserSerializer, UpdateUserSerializer
from apps.user.models import IndividualUser


class IndividualUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = IndividualUser
        fields = ('ip_name', 'iin', 'user')


class CreateIndividualUserSerializer(IndividualUserSerializer):
    user = CreateUserSerializer(many=False)


class DetailIndividualUserSerializer(IndividualUserSerializer):
    user = DetailUserSerializer(many=False)


class UpdateIndividualUserSerializer(IndividualUserSerializer):
    user = UpdateUserSerializer(many=False)
