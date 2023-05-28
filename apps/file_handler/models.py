from django.core.validators import FileExtensionValidator
from django.db import models
from django_extensions.db.models import TimeStampedModel

from apps.user.models import User


class TemplateExcel(TimeStampedModel):
    name = models.CharField(
        max_length=256,
        default='Name')
    file = models.FileField(
        upload_to='template_files',
        null=True,
        validators=[FileExtensionValidator(
        allowed_extensions=['xlsx', 'xlsm', 'xlsb', 'xltx', 'xls']
        )])
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        null=True
    )
    template_type = models.BooleanField(null=True)

    def __str__(self):
        return self.name


class MacrosExcel(TimeStampedModel):
    name = models.CharField(
        max_length=256,
        default='Name')
    macro_file = models.FileField(
        upload_to='macros_files',
        null=True,
        validators=[FileExtensionValidator(
        allowed_extensions=['xlsm',]
        )])
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        null=True
    )
    macro_type = models.BooleanField(null=True)

    def __str__(self):
        return self.name


class DataExcel(TimeStampedModel):
    name = models.CharField(
        max_length=256,
        default='Name')
    file = models.FileField(
        upload_to='data_files',
        null=True,
        validators=[FileExtensionValidator(
        allowed_extensions=['xlsx', 'xlsm', 'xlsb', 'xltx', 'xls']
        )])
    template = models.ForeignKey(
        TemplateExcel,
        verbose_name='Template id',
        on_delete=models.CASCADE)
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )

    def __str__(self):
        return self.name
