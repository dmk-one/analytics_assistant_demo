# Generated by Django 3.2.16 on 2022-11-21 06:10

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0004_alter_user_phone_number'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='admin',
        ),
    ]
