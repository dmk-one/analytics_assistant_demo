from rest_framework.routers import DefaultRouter
from django.urls import re_path
from apps.user.views import CustomUserViewSet, CustomTokenObtainPairView

router = DefaultRouter()
router.register("", CustomUserViewSet)

urlpatterns = router.urls

custom_jwt_create = re_path(r"^jwt/create/?", CustomTokenObtainPairView.as_view(), name="jwt-create")
