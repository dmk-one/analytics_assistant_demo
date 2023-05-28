from rest_framework import serializers

from .constants import SERVICE_PLAN_TYPE_CHOICES
from .models import ServicePlan, ServicePlanPayment


class ServicePlanSerializer(serializers.ModelSerializer):
    # type = serializers.ChoiceField(SERVICE_PLAN_TYPE_CHOICES.choices)

    class Meta:
        model = ServicePlan
        fields = '__all__'


class UserServicePlanPaymentSerializer(serializers.ModelSerializer):
    service_plan = serializers.SerializerMethodField()
    service_plan_name = serializers.CharField(source='service_plan.name')

    class Meta:
        model = ServicePlanPayment
        fields = (
            'user',
            'date',
            'service_plan_status',
            'payment_status',
            'method',
            'service_plan',
            'service_plan_name',
            'created',
            'modified'
        )

    def get_service_plan(self, obj):
        if hasattr(obj, 'service_plan'):
            service_plan = obj.service_plan
            return ServicePlanSerializer(service_plan).data


class ServicePlanPaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = ServicePlanPayment
        fields = '__all__'


class ServicePlanPaymentDetailSerializer(serializers.ModelSerializer):
    service_plan_name = serializers.CharField(source='service_plan.name')

    class Meta:
        model = ServicePlanPayment
        fields = (
            'user',
            'service_plan_status',
            'payment_status',
            'method',
            'service_plan_name',
            'created',
            'modified'
        )
