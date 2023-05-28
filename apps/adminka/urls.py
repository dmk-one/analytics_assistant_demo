from rest_framework.routers import DefaultRouter

from apps.adminka.views import Admin

router = DefaultRouter()
router.register("", Admin)

urlpatterns = router.urls