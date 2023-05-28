from django.utils import timezone
from rest_framework import serializers
from rest_framework.serializers import Serializer
from djoser.serializers import UserSerializer

from apps.user.models import User
from apps.notification.models import Application


class AdminApplicationSerializer(serializers.ModelSerializer):
    fio = serializers.SerializerMethodField(required=False)
    phone_number = serializers.SerializerMethodField(required=False)
    #department = serializers.SerializerMethodField(required=False)

    class Meta:
        model = Application
        fields = [
            'fio',
            'phone_number',
            #'department',
            'email',
            'created',
            'message',
        ]

    def get_fio(self, obj):
        if obj.author:
            sender_fio = obj.author.fio
            return sender_fio
        return None

    def get_phone_number(self, obj):
        if obj.author:
            if obj.author.phone_number:
                return str(obj.author.phone_number)
        return None

    # def get_departemnt(self, obj):
    #     return 'Department'


class UserApplicationSerializer(serializers.ModelSerializer):
    admin_user = serializers.IntegerField(required=False)
    author = serializers.IntegerField(required=False)

    class Meta:
        model = Application
        fields = [
            'id',
            'admin_user',
            'author',
            'name',
            'email',
            'theme',
            'message',
            'created'
        ]

    def create(self, validated_data):

        admin_user = validated_data.pop('admin_user', None)
        author = validated_data.pop('author', None)
        print(f'admin_user {admin_user}')
        if User.objects.filter(id=admin_user).exists():
            if User.objects.filter(id=admin_user).first().is_admin:
                admin_obj = User.objects.filter(id=admin_user).first()
        if User.objects.filter(id=author).exists():
            author_obj = User.objects.filter(id=author).first()

        application = Application.objects.create(         # noqa
            admin_user=admin_obj,           # noqa
            author=author_obj,              # noqa
            **validated_data
        )
        validated_data.setdefault('id', application.id)
        validated_data.setdefault('admin_user', admin_user)
        validated_data.setdefault('author', author)
        return validated_data

class UserDetailApplicationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Application
        fields = [
            'id',
            'admin_user',
            'author',
            'name',
            'email',
            'theme',
            'message',
            'created'
        ]

class UserListApplicationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Application
        fields = [
            'id',
            'admin_user',
            'author',
            'name',
            'email',
            'theme',
            'message',
            'created'
        ]