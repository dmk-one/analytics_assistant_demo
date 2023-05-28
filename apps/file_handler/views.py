import random
import os
import requests

from zipfile import ZipFile

from django.core.files.uploadedfile import InMemoryUploadedFile
from django.db.models import Q
from django.http import FileResponse
from rest_framework.decorators import action
from rest_framework import viewsets, status
from rest_framework.parsers import MultiPartParser
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from project_analyte.settings import base
from apps.user.permissions import IsAdmin, IsAuthenticatedAndOwner
from apps.user.models import User, EmployeeUser
from .models import DataExcel, TemplateExcel, MacrosExcel
from .serializers import DataExcelSerializer, TemplateExcelSerializer, MultipleTemplateExcelSerializer, \
    MacroFileSerializer, SourceFilesSerializer

from project_analyte.settings.local import NGROK_URL


class DataExcelViewSet(viewsets.ModelViewSet):
    serializer_class = DataExcelSerializer
    queryset = DataExcel.objects.all()
    permission_classes = (IsAuthenticatedAndOwner,)
    parser_classes = (MultiPartParser,)

    def get_queryset(self, *args, **kwargs):
        return DataExcel.objects.all().filter(user=self.request.user)

    @action(methods=['POST'], detail=False, url_path='upload')
    def upload(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    @action(methods=['GET'], detail=True, url_path='download')
    def download(self, request, *args, **kwargs):
        obj = self.get_object()
        path = obj.file.path
        filename = obj.file.name

        response = FileResponse(
            open(path, "rb"),
            filename=filename,
            as_attachment=True,
            content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
        )
        response['Access-Control-Expose-Headers'] = 'Content-Disposition'
        return response

    @action(methods=['GET'], detail=True, url_path='insert_into_template')
    def insert_into_template(self, request, *args, **kwargs):
        data_excel_object = self.get_object()
        data_excel_path = data_excel_object.file.path

        template_excel_path = data_excel_object.template.file.path
        print(f'data_excel_path {data_excel_path}')
        print(f'template_excel_path {template_excel_path}')
        print('*******************************************')

        url = f'{NGROK_URL}/?data_excel_id={data_excel_object.id}&' \
              f'template_excel_id={data_excel_object.template.id}'

        with open(data_excel_path, 'rb') as data_excel, open(template_excel_path, 'rb') as template_excel:
            excel_files = [
                ('data_excel', data_excel),
                ('template_excel', template_excel)
            ]
            print('before')
            response = requests.request("POST", url, files=excel_files)
            print('after')
            ready_path = os.path.join(base.MEDIA_ROOT, 'ready/')

            if not os.path.exists(ready_path):
                os.mkdir(ready_path)

            path = os.path.join(ready_path,
                                f'ready_data_{data_excel_object.id}_template_{data_excel_object.template.id}.xlsx'
                                )

            with open(path, "wb") as binary_file:
                binary_file.write(response.content)

            response = FileResponse(
                open(path, 'rb'),
                filename='ready.xlsx',
                as_attachment=True,
                content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
            )

            response['Access-Control-Expose-Headers'] = 'Content-Disposition'
            return response


class TemplateExcelViewSet(viewsets.ModelViewSet):
    serializer_class = TemplateExcelSerializer
    queryset = TemplateExcel.objects.all()
    permission_classes = (IsAuthenticated,)
    parser_classes = (MultiPartParser,)

    def get_permissions(self):
        if self.action == "destroy":
            self.permission_classes = [IsAdmin]
        return super().get_permissions()

    def get_queryset(self, *args, **kwargs):
        return TemplateExcel.objects.all()

    @action(methods=['GET'], detail=False, url_path='get_public_templates')
    def get_public_templates(self, request, *args, **kwargs):
        public_templates = TemplateExcel.objects.filter(template_type=False)
        serializer = self.get_serializer(public_templates, many=True)

        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_200_OK, headers=headers)

    @action(methods=['GET'], detail=False, url_path='get_individual_templates')
    def get_individual_templates(self, request, *args, **kwargs):
        if User.objects.filter(Q(employee_user__isnull=False) \
                               & Q(id=request.user.id)):
            employee_user = EmployeeUser.objects.filter(user=request.user).first()
            individual_templates = TemplateExcel.objects.filter(template_type=True, user=employee_user.juridical)
        else:
            individual_templates = TemplateExcel.objects.filter(template_type=True, user=request.user)

        serializer = self.get_serializer(individual_templates, many=True)

        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    @action(methods=['POST'], detail=False, url_path='upload', permission_classes=[IsAdmin])
    def upload(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        serializer.save()

        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    @action(methods=['POST'], detail=False, url_path='upload_multiple',
            permission_classes=[IsAdmin], serializer_class=MultipleTemplateExcelSerializer)
    def upload_multiple(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        templates: InMemoryUploadedFile = request.data['templates']

        template_names = []
        templates_directory = base.MEDIA_ROOT + '/template_files/'

        with ZipFile(templates.file, "r") as myzip:
            for item in myzip.infolist():
                template_names.append(item.filename)
                myzip.extract(path=templates_directory, member=item.filename)

        for index in range(0, len(template_names)):
            new_file_name = str(random.randint(11111, 99999)) + template_names[index]
            os.rename(templates_directory + template_names[index], templates_directory + new_file_name)
            template_names[index] = new_file_name

        bulk_create_data = []

        for template_name in template_names:
            bulk_create_data.append(TemplateExcel(
                file=f'template_files/{template_name}',
                template_type=serializer['template_type'].value,  # serializer['template_type'] - BoundField
                user=User.objects.filter(id=serializer['user'].value).first()  # serializer['user'] - BoundField
            ))

        new_template_records = TemplateExcel.objects.bulk_create(bulk_create_data)
        serializer = TemplateExcelSerializer(new_template_records, many=True)

        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    @action(methods=['GET'], detail=True, url_path='download', permission_classes=[IsAdmin])
    def download(self, request, *args, **kwargs):
        obj = self.get_object()
        path = obj.file.path
        filename = obj.file.name

        response = FileResponse(
            open(path, "rb"),
            filename=filename,
            as_attachment=True,
            content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
        )
        response['Access-Control-Expose-Headers'] = 'Content-Disposition'
        return response

    @action(
        methods=['POST'], detail=False, url_path='upload_macro_file',
        permission_classes=[IsAdmin], serializer_class=MacroFileSerializer
    )
    def upload_macro_file(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        # macro_file: InMemoryUploadedFile = request.data['macro_file']
        #
        # url = '{NGROK_URL}/upload_macro_file/'
        # macro_file = [
        #     ('macro_file', macro_file),
        # ]
        #
        # response = requests.request("POST", url, files=macro_file)
        # return Response(response.json(), status=status.HTTP_200_OK)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    @action(
        methods=['POST'], detail=False, url_path='convert_source_files',
        serializer_class=SourceFilesSerializer
    )
    def convert_source_files(self, request, *args, **kwargs):
        source_files: InMemoryUploadedFile = request.data['source_files']
        macro_file_id = request.data['macro_file_id']

        macro_file_obj = MacrosExcel.objects.filter(id=macro_file_id).first()

        with open(macro_file_obj.macro_file.path, 'rb') as macro_file:
            macro_and_source_files = [
                ('macro_file', macro_file),
                ('source_files', source_files),
            ]

            url = f'{NGROK_URL}/convert_source_files/'

            response = requests.request("POST", url, files=macro_and_source_files)

        converted_path = os.path.join(base.MEDIA_ROOT, 'converted/')

        if not os.path.exists(converted_path):
            os.mkdir(converted_path)

        converted_path = os.path.join(converted_path, 'converted.zip')

        with open(converted_path, "wb") as binary_file:
            binary_file.write(response.content)

        response = FileResponse(
            open(converted_path, 'rb'),
            filename='converted.zip',
            as_attachment=True,
            content_type='application/zip'
        )
        response['Access-Control-Expose-Headers'] = 'Content-Disposition'

        return response

    # @action(methods=['POST'], detail=False, url_path='convert_source_file',
    #         permission_classes=[IsAuthenticated], serializer_class=SourceFileSerializer)
    # def convert_source_file(self, request, *args, **kwargs):
    #     source_file: InMemoryUploadedFile = request.data['source_file']
    #
    #     url = 'https://{NGROK_URL}/convert_source_file/'
    #     source_file = [
    #         ('source_file', source_file),
    #     ]
    #
    #     response = requests.request("POST", url, files=source_file)
    #     converted_path = os.path.join(base.MEDIA_ROOT, 'converted/')
    #
    #     if not os.path.exists(converted_path):
    #         os.mkdir(converted_path)
    #     converted_path = os.path.join(converted_path, 'converted.xls')
    #
    #     with open(converted_path, "wb") as binary_file:
    #         binary_file.write(response.content)
    #     response = FileResponse(
    #         open(converted_path, 'rb'),
    #         filename='converted.xls',
    #         as_attachment=True,
    #         content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    #     )
    #     response['Access-Control-Expose-Headers'] = 'Content-Disposition'
    #
    #     return response

    @action(
        methods=['GET'], detail=False, url_path='get_macro_file_names',
        permission_classes=[IsAuthenticated], serializer_class=MacroFileSerializer
    )
    def get_macro_file_names(self, request, *args, **kwargs):
        macro_files = MacrosExcel.objects.filter(user=request.user)
        serializer = self.get_serializer(macro_files, many=True)

        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_200_OK, headers=headers)
