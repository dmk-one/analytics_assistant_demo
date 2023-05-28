from django.shortcuts import render
from django.db.models import Q
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.viewsets import GenericViewSet
from rest_framework.response import Response

from apps.adminka.models import News
from apps.adminka.serializers import NewsSerializer, AdminUserList, UpdateUserStatus, AdminDetailUserSerializer
from apps.user.models import User
from apps.user.permissions import IsAdmin
from apps.user.serializers import DetailUserSerializer, SimpleUserSerializer


class Admin(viewsets.ModelViewSet):
    queryset = User.objects.all()
    permission_classes = (IsAdmin,)
    serializer_class = SimpleUserSerializer

    @action(["get"], detail=False, serializer_class=AdminUserList)
    def user_list(self, request, *args, **kwargs):
        all_juridical_and_individual_users = User.objects.filter(
            Q(juridical_user__isnull=False) | Q(individual_user__isnull=False)
        )
        serializer = self.get_serializer(all_juridical_and_individual_users, many=True)

        return Response(serializer.data)

    @action(["post"], detail=True, serializer_class=UpdateUserStatus)
    def update_user_status(self, request, *args, **kwargs):
        is_active = request.data.pop('is_active', None)
        user = User.objects.filter(pk=kwargs['pk']).first()

        if user is None:
            return Response(None, status=status.HTTP_404_NOT_FOUND)
        if is_active is not None:
            user.is_active = is_active
            user.save()
            return Response(AdminDetailUserSerializer(user).data, status=status.HTTP_200_OK)

    @action(["get"], detail=True, serializer_class=AdminDetailUserSerializer)
    def user_detail(self, request, *args, **kwargs):
        user = User.objects.get(pk=kwargs['pk'])
        serializer = self.get_serializer(user, many=False)
        return Response(serializer.data)

    @action(["POST"], detail=False, serializer_class=NewsSerializer)
    def publish_news(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    @action(["POST"], detail=True, serializer_class=NewsSerializer)
    def update_news(self, request, *args, **kwargs):
        news = News.objects.filter(pk=kwargs['pk']).first()

        for key, value in request.data.items():
            setattr(news, key, value)

        news.save()

        serializer = self.get_serializer(news)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(["GET"], detail=True, serializer_class=NewsSerializer)
    def disable_news(self, request, *args, **kwargs):
        news = News.objects.filter(pk=kwargs['pk']).first()
        news.is_published = False
        news.save()

        serializer = self.get_serializer(news)

        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(["GET"], detail=True, serializer_class=NewsSerializer)
    def enable_news(self, request, *args, **kwargs):
        news = News.objects.filter(pk=kwargs['pk']).first()
        news.is_published = True
        news.save()

        serializer = self.get_serializer(news)

        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(["GET"], detail=True, serializer_class=NewsSerializer)
    def detail_news(self, request, *args, **kwargs):
        news = News.objects.filter(pk=kwargs['pk']).first()

        serializer = self.get_serializer(news)

        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(["GET"], detail=True, serializer_class=NewsSerializer)      # FIX Why GET ?
    def delete_news(self, request, *args, **kwargs):
        News.objects.filter(pk=kwargs['pk']).delete()

        return Response(None, status=status.HTTP_200_OK)


    # @action(["POST"], detail=False, serializer_class=NotificationSerializer)
    # def send_notification_for_all_users(self, request, *args, **kwargs):
    #     serializer = self.get_serializer(data=request.data)
    #     serializer.is_valid(raise_exception=True)
    #     users_id_list = User.objects.filter(~Q(id=request.user.id)).values_list('id', flat=True)
    #
    #     data = dict(serializer.data)
    #     data['for_users'] = list(users_id_list)
    #
    #     print(data)
    #
    #     detail_serializer = NotificationDetailSerializer(data=data)
    #     detail_serializer.is_valid(raise_exception=True)
    #     detail_serializer.save()
    #
    #     print('detail_serializer.data', detail_serializer.data)
    #     headers = self.get_success_headers(detail_serializer.data)
    #     return Response(detail_serializer.data, status=status.HTTP_201_CREATED, headers=headers)







