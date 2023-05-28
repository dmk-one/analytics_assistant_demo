from django.db import models
from django.utils.translation import gettext_lazy as _
from django_extensions.db.models import TimeStampedModel
from datetime import datetime

from apps.payments.constants import STATUS_CHOICES, METHOD_CHOICES, SERVICE_PLAN_TYPE_CHOICES
from django.utils import timezone
from apps.user.models import User


class ServicePlan(TimeStampedModel):
    name = models.CharField(max_length=256)
    type = models.CharField(max_length=10, choices=SERVICE_PLAN_TYPE_CHOICES.choices)
    price = models.IntegerField(null=False, default=0)
    max_user = models.SmallIntegerField(null=False, default=0)
    expiration_days = models.SmallIntegerField()


# class BalanceReplenishment(models.Model):
#     user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='balance_replenishment_log')
#     status = models.CharField(max_length=10, choices=STATUS_CHOICES.choices, default="UNKNOWN")
#     method = models.CharField(max_length=10, choices=METHOD_CHOICES.choices, default="UNKNOWN")
#     amount = models.IntegerField(null=False, default=0)
#     date = models.DateTimeField(_('date'), default=timezone.now)
#
#     class Meta:
#         ordering = ('-date',)


class ServicePlanPayment(TimeStampedModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='service_plan_payments')
    service_plan_status = models.BooleanField(default=False)
    payment_status = models.CharField(max_length=10, choices=STATUS_CHOICES.choices, default="UNKNOWN")
    method = models.CharField(max_length=10, choices=METHOD_CHOICES.choices, default="UNKNOWN")
    service_plan = models.ForeignKey(ServicePlan, on_delete=models.CASCADE, related_name='payments')
    date = models.DateTimeField(default=datetime.now())

    class Meta:
        ordering = ('-created', )

    def get_service_plan_status(self):
        service_plan_delta = timezone.timedelta(days=self.service_plan.expiration_days)
        current_delta = timezone.now() - self.created
        return True if service_plan_delta > current_delta else False

    def update_service_plan_status(self):
        self.service_plan_status = self.get_service_plan_status()
