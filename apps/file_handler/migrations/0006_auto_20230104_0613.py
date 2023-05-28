# Generated by Django 3.2.16 on 2023-01-04 06:13

from django.db import migrations
import django.utils.timezone
import django_extensions.db.fields


class Migration(migrations.Migration):

    dependencies = [
        ('file_handler', '0005_alter_templateexcel_user'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='dataexcel',
            options={'get_latest_by': 'modified'},
        ),
        migrations.AlterModelOptions(
            name='templateexcel',
            options={'get_latest_by': 'modified'},
        ),
        migrations.AddField(
            model_name='dataexcel',
            name='created',
            field=django_extensions.db.fields.CreationDateTimeField(auto_now_add=True, default=django.utils.timezone.now, verbose_name='created'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='dataexcel',
            name='modified',
            field=django_extensions.db.fields.ModificationDateTimeField(auto_now=True, verbose_name='modified'),
        ),
        migrations.AddField(
            model_name='templateexcel',
            name='created',
            field=django_extensions.db.fields.CreationDateTimeField(auto_now_add=True, default=django.utils.timezone.now, verbose_name='created'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='templateexcel',
            name='modified',
            field=django_extensions.db.fields.ModificationDateTimeField(auto_now=True, verbose_name='modified'),
        ),
    ]