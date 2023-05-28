import random
from typing import Dict

from django.contrib.auth.models import Group
from django.db.models import Q
from django.contrib.auth.hashers import make_password
from djoser.views import UserViewSet
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView

from apps.adminka.serializers import News
from apps.adminka.serializers import NewsSerializer
from .models import JuridicalUser, IndividualUser, User, UserVerificationCode, EmployeeUser
from .serializers import \
    SimpleUserSerializer, DetailUserSerializer, \
    CreateIndividualUserSerializer, DetailIndividualUserSerializer, UpdateIndividualUserSerializer, \
    CreateJuridicalUserSerializer, DetailJuridicalUserSerializer, UpdateJuridicalUserSerializer, \
    CreateEmployeeUserSerializer, DetailEmployeeUserSerializer, UpdateEmployeeUserSerializer, \
    VerificationCodeSerializer, ResetPasswordSerializer
from .permissions import IsAdmin, IsJuridical
from .serializers.jwt import CustomTokenObtainPairSerializer
from .utils import MailSender, new_password_generator
from .tasks import create_verif_code_and_send_mail, send_password_to_employee_mail


class CustomUserViewSet(UserViewSet):

    serializer_class = SimpleUserSerializer

    def _make_user(self, data: dict) -> Dict:
        user_data = data.pop('user')
        new_user = User.objects.create_user(**user_data)
        data['user'] = new_user
        return data

    def make_response(self, response_data):
        headers = self.get_success_headers(response_data)
        return Response(response_data, status=status.HTTP_201_CREATED,
                        headers=headers)

    def update_user_and_role(self, user_obj, role_obj, data_to_update: dict):
        user_data = data_to_update.pop('user', {})
        new_password = user_data.pop('password', False)
        role_data = data_to_update

        for key, value in user_data.items():
            setattr(user_obj, key, value)

        for key, value in role_data.items():
            setattr(role_obj, key, value)

        if new_password:
            user_obj.password = make_password(new_password)

        user_obj.save()
        role_obj.save()

        return role_obj

    @action(["get"], detail=False, permission_classes=[IsAdmin])
    def all_user_list(self, request, *args, **kwargs):
        queryset = User.objects.filter(~Q(id=request.user.id))
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    @action(["get"], detail=False, permission_classes=[IsJuridical], serializer_class=DetailEmployeeUserSerializer)
    def employee_user_list(self, request, *args, **kwargs):
        current_user = request.user
        queryset = EmployeeUser.objects.filter(juridical=current_user)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    @action(["get"], detail=True, permission_classes=[IsAdmin], serializer_class=DetailUserSerializer)
    def user_detail(self, request, *args, **kwargs):
        queryset = User.objects.get(id=kwargs['id'])
        serializer = DetailUserSerializer(queryset, many=False)
        return Response(serializer.data)

    @action(["post"], detail=False, permission_classes=[AllowAny], serializer_class=CreateJuridicalUserSerializer)
    def create_juridical_user(self, request, **kwargs):
        juridical_serializer = self.get_serializer(data=request.data)
        juridical_serializer.is_valid(raise_exception=True)
        juridical_data_with_user = self._make_user(request.data)
        juridical_group, created = Group.objects.get_or_create(name='juridical')
        new_juridical_user = JuridicalUser.objects.create(**juridical_data_with_user)
        new_juridical_user.user.groups.set([juridical_group])

        create_verif_code_and_send_mail.delay(new_juridical_user.user.id) # Celery

        return self.make_response(DetailJuridicalUserSerializer(new_juridical_user).data)

    @action(["post"], detail=False, permission_classes=[AllowAny], serializer_class=CreateIndividualUserSerializer)
    def create_individual_user(self, request, *args, **kwargs):
        individual_serializer = self.get_serializer(data=request.data)
        individual_serializer.is_valid(raise_exception=True)
        individual_data_with_user = self._make_user(request.data)
        individual_group, created = Group.objects.get_or_create(name='individual')
        new_individual_user = IndividualUser.objects.create(**individual_data_with_user)
        new_individual_user.user.groups.set([individual_group])

        create_verif_code_and_send_mail.delay(new_individual_user.user.id) # Celery

        return self.make_response(DetailIndividualUserSerializer(new_individual_user).data)

    @action(["post"], detail=False, permission_classes=[IsJuridical | IsAdmin], serializer_class=CreateEmployeeUserSerializer)
    def create_employee_user(self, request, *args, **kwargs):
        employee_serializer = self.get_serializer(data=request.data)
        employee_serializer.is_valid(raise_exception=True)
        new_password = new_password_generator()
        new_employee_data = {
            'user': {
                'email': employee_serializer.data['email'],
                'fio': f'Name_{random.randint(10000, 99999)}',
                'password': new_password,
                'is_active': True
            },
            'juridical': request.user
        }
        employee_data_with_user = self._make_user(new_employee_data)
        employee_group, created = Group.objects.get_or_create(name='employee')
        new_employee_user = EmployeeUser.objects.create(**employee_data_with_user)
        new_employee_user.user.groups.set([employee_group])

        send_password_to_employee_mail.delay(
            new_password=new_password,
            recipient_email=new_employee_user.user.email
        ) # Celery

        return self.make_response(DetailEmployeeUserSerializer(new_employee_user).data)

    @action(["post"], detail=False, permission_classes=[AllowAny], serializer_class=VerificationCodeSerializer)
    def activate_new_user(self, request, *args, **kwargs):
        activation_code_serializer = self.get_serializer(data=request.data)
        activation_code_serializer.is_valid(raise_exception=True)
        user_verification_object = UserVerificationCode.objects.get(
            code=activation_code_serializer.data['code']
        )
        activated_user = User.objects.get(email=user_verification_object.user.email)
        activated_user.is_active = True
        activated_user.save()
        user_verification_object.delete()
        user_serializer = SimpleUserSerializer(activated_user)

        return self.make_response(user_serializer.data)

    @action(["post"], detail=False, permission_classes=[AllowAny], serializer_class=ResetPasswordSerializer)
    def reset_password(self, request, *args, **kwargs):
        reset_password_serializer = self.get_serializer(data=request.data)
        reset_password_serializer.is_valid(raise_exception=True)
        new_password = new_password_generator()
        user = User.objects.get(email=reset_password_serializer.data['email'])
        user.password = make_password(new_password)
        user.save()
        MailSender().send_reset_password_mail(
            new_password=new_password,
            recipient=user.email
        )
        user_serializer = SimpleUserSerializer(user)

        return self.make_response(user_serializer.data)

    @action(["get"], detail=False)
    def me(self, request, *args, **kwargs):
        serializer = None
        user = None
        user_type = None

        if hasattr(request.user, 'juridical_user'):
            user = request.user.juridical_user
            serializer = DetailJuridicalUserSerializer
            user_type = 'juridical_user'
        if hasattr(request.user, 'individual_user'):
            user = request.user.individual_user
            serializer = DetailIndividualUserSerializer
            user_type = 'individual_user'
        if hasattr(request.user, 'employee_user'):
            user = request.user.employee_user
            serializer = DetailEmployeeUserSerializer
            user_type = 'employee_user'

        response_data = dict(serializer(user).data)
        response_data['user_type'] = user_type

        return self.make_response(response_data)

    @action(["put"], detail=False, permission_classes=[IsAuthenticated], serializer_class=UpdateJuridicalUserSerializer)
    def update_juridical_user(self, request, *args, **kwargs):
        user = User.objects.get(id=request.user.id)
        juridical_user = self.update_user_and_role(
            user_obj=user,
            role_obj=user.juridical_user,
            data_to_update=request.data
        )
        serializer = self.get_serializer(juridical_user)

        return self.make_response(serializer.data)

    @action(["put"], detail=False, permission_classes=[IsAuthenticated], serializer_class=UpdateIndividualUserSerializer)
    def update_individual_user(self, request, *args, **kwargs):
        user = User.objects.get(id=request.user.id)
        individual_user = self.update_user_and_role(
            user_obj=user,
            role_obj=user.individual_user,
            data_to_update=request.data
        )
        serializer = self.get_serializer(individual_user)

        return self.make_response(serializer.data)

    @action(["put"], detail=False, permission_classes=[IsAuthenticated], serializer_class=UpdateEmployeeUserSerializer)
    def update_employee_user(self, request, *args, **kwargs):
        user = User.objects.get(id=request.user.id)
        employee_user = self.update_user_and_role(
            user_obj=user,
            role_obj=user.employee_user,
            data_to_update=request.data
        )
        serializer = self.get_serializer(employee_user)

        return self.make_response(serializer.data)

    @action(["delete"], detail=True, permission_classes=[IsAuthenticated])
    def delete_user(self, request, *args, **kwargs):
        user = User.objects.get(id=request.user.id)

        if user.is_admin:
            User.objects.filter(id=kwargs['id']).delete()
            return Response(True, status=status.HTTP_200_OK)

        if hasattr(user, 'juridical_user'):
            employee = User.objects.filter(id=kwargs['id']).first()
            if employee.employee_user.juridical == user:
                employee.delete()
                return Response(True, status=status.HTTP_200_OK)

        return Response(False, status=status.HTTP_404_NOT_FOUND)

    @action(["get"], detail=False, permission_classes=[IsAuthenticated], serializer_class=NewsSerializer)
    def news_list(self, request, *args, **kwargs):
        news = News.objects.all()
        serializer = self.get_serializer(news, many=True)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_200_OK, headers=headers)

class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer
