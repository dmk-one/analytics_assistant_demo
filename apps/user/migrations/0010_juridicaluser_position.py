# Generated by Django 3.2.16 on 2022-12-02 12:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0009_auto_20221202_1159'),
    ]

    operations = [
        migrations.AddField(
            model_name='juridicaluser',
            name='position',
            field=models.CharField(max_length=255, null=True),
        ),
    ]