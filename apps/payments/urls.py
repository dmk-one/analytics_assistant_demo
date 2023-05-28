from rest_framework.routers import DefaultRouter

from apps.payments.views import PaymentsViewSet, ServicePlanViewSet

router = DefaultRouter()
router.register(r'payments', PaymentsViewSet, basename='payments')
router.register(r'service_plan', ServicePlanViewSet, basename='service_plan')

urlpatterns = router.urls
