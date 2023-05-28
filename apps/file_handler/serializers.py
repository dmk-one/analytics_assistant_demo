from rest_framework import serializers
from .models import DataExcel, TemplateExcel, MacrosExcel
from ..user.serializers import User


class TemplateExcelSerializer(serializers.ModelSerializer):
    template_type = serializers.BooleanField(required=False)

    class Meta:
        model = TemplateExcel
        fields = (
            'id',
            'created',
            'name',
            'user',
            'template_type',
            'file'
        )


class MultipleTemplateExcelSerializer(serializers.Serializer):
    template_type = serializers.BooleanField(required=False)
    templates = serializers.FileField()
    user = serializers.IntegerField()

    def validate_user(self, value):
        if User.objects.filter(id=value).exists():
            return value
        raise serializers.ValidationError(f"Пользователь с id - {value} не существует")


class DataExcelSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = DataExcel
        fields = '__all__'


class MacroFileSerializer(serializers.ModelSerializer):
    class Meta:
        model = MacrosExcel
        fields = (
            'id',
            'created',
            'name',
            'user',
            'macro_type',
            'macro_file'
        )


class SourceFilesSerializer(serializers.Serializer):
    source_files = serializers.FileField()
    macro_file_id = serializers.IntegerField()
    # macrofile_name = serializers.CharField(max_length=100)


# class SourceFileSerializer(serializers.Serializer):
#     source_file = serializers.FileField()
