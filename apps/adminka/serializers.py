from rest_framework import serializers
from rest_framework.serializers import Serializer
from djoser.serializers import UserSerializer

from apps.adminka.models import News
from apps.payments.serializers import UserServicePlanPaymentSerializer
from apps.user.models import User


class NewsSerializer(serializers.ModelSerializer):
    admin = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = News
        fields = ('id','title', 'body', 'is_published', 'admin', 'publish_date')


class AdminUserList(serializers.ModelSerializer):
    user_type = serializers.SerializerMethodField()
    fio_company_name = serializers.SerializerMethodField()
    iin_bin = serializers.SerializerMethodField()
    active_payment = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ('user_type',
                  'id',
                  'fio_company_name',
                  'phone_number',
                  'email',
                  'iin_bin',
                  'is_active',
                  'spent_balance',
                  'date_joined',
                  'active_payment')

    def get_user_type(self, obj):
        if hasattr(obj, 'individual_user'):
            return 'individual_user'
        if hasattr(obj, 'juridical_user'):
            return 'juridical_user'

    def get_active_payment(self, obj):
        if hasattr(obj, 'service_plan_payments'):
            last_payment = obj.service_plan_payments.order_by('created').last()
            return UserServicePlanPaymentSerializer(last_payment).data

    def get_fio_company_name(self, obj):
        if hasattr(obj, 'individual_user'):
            return obj.fio
        if hasattr(obj, 'juridical_user'):
            return obj.juridical_user.company_name

    def get_iin_bin(self, obj):
        if hasattr(obj, 'individual_user'):
            return obj.individual_user.iin
        if hasattr(obj, 'juridical_user'):
            return obj.juridical_user.bin


class AdminDetailUserSerializer(UserSerializer):
    payment_log = serializers.SerializerMethodField()
    user_type = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = tuple(User.REQUIRED_FIELDS) + (
            'id',
            'email',
            'balance',
            'spent_balance',
            'is_admin',
            'date_joined',
            'is_active',
            'payment_log',
            'user_type'
        )

    def get_payment_log(self, obj):
        if hasattr(obj, 'payment_log'):
            success_payment_log_list = obj.payment_log.filter(status='success').values()
            if len(success_payment_log_list) > 0:
                return success_payment_log_list[0]
        return None

    def get_user_type(self, obj):
        if hasattr(obj, 'juridical_user'):
            return 'juridical'
        if hasattr(obj, 'individual_user'):
            return 'individual'


class UpdateUserStatus(Serializer):
    is_active = serializers.BooleanField(default=True)
