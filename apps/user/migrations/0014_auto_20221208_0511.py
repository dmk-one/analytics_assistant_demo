# Generated by Django 3.2.16 on 2022-12-08 05:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0013_auto_20221207_0441'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='paymentlog',
            options={'ordering': ('-date',)},
        ),
        migrations.AddField(
            model_name='paymentlog',
            name='next_payment_date',
            field=models.DateTimeField(default=None, null=True, verbose_name='date'),
        ),
    ]
