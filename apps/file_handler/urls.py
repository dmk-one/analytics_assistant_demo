from rest_framework.routers import DefaultRouter

from apps.file_handler.views import DataExcelViewSet, TemplateExcelViewSet

router = DefaultRouter()
router.register(r'data_excel', DataExcelViewSet, basename='data_excel')
router.register(r'template_excel', TemplateExcelViewSet, basename='template_excel')
