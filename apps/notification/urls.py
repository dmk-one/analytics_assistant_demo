from rest_framework.routers import DefaultRouter

from apps.notification.views import AdminApplicationViewSet, UserApplicationViewSet

router = DefaultRouter()
router.register(r'admin_application', AdminApplicationViewSet, basename='admin_application')
router.register(r'user_application', UserApplicationViewSet, basename='user_application')

urlpatterns = router.urls
