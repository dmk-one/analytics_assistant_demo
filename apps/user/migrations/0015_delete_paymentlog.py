# Generated by Django 3.2.16 on 2023-01-26 10:48

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0014_auto_20221208_0511'),
    ]

    operations = [
        migrations.DeleteModel(
            name='PaymentLog',
        ),
    ]