from rest_framework import serializers
from .base import DetailUserSerializer, UpdateUserSerializer
from ..models import EmployeeUser


class EmployeeUserSerializer(serializers.ModelSerializer):
    company_name = serializers.CharField(source='juridical.juridical_user.company_name')

    class Meta:
        model = EmployeeUser
        fields = ('position', 'company_name', 'juridical', 'user')


class DetailEmployeeUserSerializer(EmployeeUserSerializer):
    user = DetailUserSerializer(many=False)


class UpdateEmployeeUserSerializer(EmployeeUserSerializer):
    user = UpdateUserSerializer(many=False)

    class Meta:
        model = EmployeeUser
        fields = ('position', 'user')


class CreateEmployeeUserSerializer(serializers.Serializer):
    email = serializers.EmailField()
