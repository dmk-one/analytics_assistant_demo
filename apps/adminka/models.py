import django
from django.utils import timezone
from django.db import models
from django_extensions.db.models import TimeStampedModel

from apps.user.models import User


class News(TimeStampedModel):
    title = models.CharField(max_length=50, null=True)
    body = models.TextField(null=True)
    publish_date = models.DateTimeField(default=django.utils.timezone.now, blank=True)
    is_published = models.BooleanField(default=True)
    admin = models.ForeignKey(User, on_delete=models.CASCADE)

#
# class Notification(models.Model):
#     notification = models.CharField(max_length=256, null=False)
#     publisher = models.ForeignKey(User, on_delete=models.CASCADE)
#     for_users = ArrayField(models.IntegerField(), null=True)
