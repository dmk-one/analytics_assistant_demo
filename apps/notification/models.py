from django.db import models
from django.utils.translation import gettext_lazy as _
from django_extensions.db.models import TimeStampedModel
from apps.user.models import User

# from user.models import User
#
#
# class Notification(models.Model):
#     user_sender = models.ForeignKey(
#         User,
#         null=True,
#         blank=True,
#         related_name='user_sender',
#         on_delete=models.CASCADE)
#     user_revoker = models.ForeignKey(
#         User,
#         null=True,
#         blank=True,
#         related_name='user_revoker',
#         on_delete=models.CASCADE
#     )
#     status = models.CharField(
#         max_length=264,
#         null=True,
#         blank=True,
#         default='unread'
#     )
#     type_of_notification = models.CharField(
#         max_length=264,
#         null=True,
#         blank=True
#     )


class Application(TimeStampedModel):
    admin_user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='admin_applications'
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='author_applications'
    )
    name = models.CharField(
        max_length=264,
        null=True,
        blank=True
    )
    email = models.EmailField(
        _('Почта'),
        unique=False,
        null=False)
    theme = models.CharField(
        max_length=264,
        null=True,
        blank=True
    )
    message = models.TextField(
        _('Сообщения')
    )