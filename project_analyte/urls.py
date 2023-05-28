from django.conf.urls.static import static
from django.conf import settings
from django.urls import path, include
from django.contrib import admin
from django.contrib.auth import views as auth_views

from drf_spectacular.views import SpectacularAPIView, SpectacularRedocView, SpectacularSwaggerView

from apps.file_handler.urls import router as file_handler_router
from djoser.urls.jwt import urlpatterns as jwt_urlpatterns
from apps.user.urls import custom_jwt_create


jwt_urlpatterns = jwt_urlpatterns[1:]
jwt_urlpatterns.append(custom_jwt_create)

api_version = 'api/v1/'

urlpatterns = [
    path(f'{api_version}swagger/', SpectacularAPIView.as_view(), name='schema'),
    # SWAGGER UI:
    path(f'{api_version}swagger/ui/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path(f'{api_version}schema/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),

    path('admin/', admin.site.urls),

    path(f'{api_version}api-auth/', include('rest_framework.urls')),

    path(f'{api_version}', include(jwt_urlpatterns)),
    path(f'{api_version}user/', include('apps.user.urls')),

    path(f'{api_version}admin/', include('apps.adminka.urls')),

    path(f'{api_version}token/logout/', auth_views.LogoutView.as_view(), name='logout'),

    path(f'{api_version}file_handler/', include(file_handler_router.urls)),
    path(f'{api_version}notification/', include('apps.notification.urls')),
    path(f'{api_version}payments/', include('apps.payments.urls')),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)