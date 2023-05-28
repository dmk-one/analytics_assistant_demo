from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from apps.user.permissions import IsAdmin
from apps.notification.models import Application
from apps.notification.serializers import AdminApplicationSerializer, UserApplicationSerializer, \
    UserDetailApplicationSerializer, UserListApplicationSerializer


class AdminApplicationViewSet(viewsets.ModelViewSet):
    queryset = Application.objects.all()
    permission_classes = (IsAdmin,)
    serializer_class = AdminApplicationSerializer
    http_method_names = ['post', 'get']

    @action(["get"], detail=False, serializer_class=AdminApplicationSerializer)
    def application_list(self, request, *args, **kwargs):
        all_applications = self.queryset.filter(admin_user=request.user.id)
        serializer = self.get_serializer(all_applications, many=True)

        return Response(serializer.data)


class UserApplicationViewSet(viewsets.ModelViewSet):
    queryset = Application.objects.all()
    serializer_class = UserApplicationSerializer
    http_method_names = ['post', 'get']

    def retrieve(self, request, *args, **kwargs):
        self.get_serializer = UserDetailApplicationSerializer
        application = self.queryset.filter(author=request.user).first()
        serializer = self.get_serializer(application)
        return Response(serializer.data)

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        self.get_serializer = UserListApplicationSerializer
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    # @action(["get"], detail=False, serializer_class=UserDetailApplicationSerializer)
    # def application_detail(self, request, *args, **kwargs):
    #     application = self.queryset.filter(author=request.user).all()
    #     serializer = self.get_serializer(application, many=True)
    #
    #     return Response(serializer.data)
