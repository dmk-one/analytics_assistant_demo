from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework import status


from apps.payments.models import ServicePlan, ServicePlanPayment
from apps.payments.serializers import ServicePlanSerializer, ServicePlanPaymentSerializer, \
    ServicePlanPaymentDetailSerializer
from apps.user.permissions import IsAdmin

from apps.user.models import User

class PaymentsViewSet(viewsets.ModelViewSet):
    queryset = ServicePlanPayment.objects.all()
    permission_classes = (IsAuthenticated,)
    serializer_class = ServicePlanPaymentSerializer

    def get_permissions(self):
        if self.action == "create":
            self.permission_classes = [IsAdmin]
        if self.action == "destroy":
            self.permission_classes = [IsAdmin]
        if self.action == "update":
            self.permission_classes = [IsAdmin]
        return super().get_permissions()

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = request.data.pop('user', None)
        service_plan = request.data.pop('service_plan', None)
        service_plan_obj = ServicePlan.objects.filter(id=service_plan).first()
        user_obj = User.objects.filter(id=user).first()
        obj_payment = ServicePlanPayment.objects.create(
            user=user_obj,
            service_plan=service_plan_obj,
            **request.data)

        headers = self.get_success_headers(serializer.data)
        return Response(ServicePlanPaymentDetailSerializer(obj_payment).data, status=status.HTTP_201_CREATED, headers=headers)



    @action(["get"], detail=False, serializer_class=ServicePlanPaymentDetailSerializer)
    def get_my_service_plan_payments(self, request, *args, **kwargs):
        my_service_plan_payments = self.queryset.filter(user=request.user.id).order_by('-created').first()
        serializer = self.get_serializer(my_service_plan_payments)

        return Response(serializer.data)


class ServicePlanViewSet(viewsets.ModelViewSet):
    queryset = ServicePlan.objects.all()
    permission_classes = (IsAdmin,)
    serializer_class = ServicePlanSerializer
