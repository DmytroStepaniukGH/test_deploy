# Generated by Django 4.1.7 on 2023-04-25 17:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('notifications', '0002_notification_appointment'),
    ]

    operations = [
        migrations.AlterField(
            model_name='notification',
            name='is_read',
            field=models.BooleanField(default=False, verbose_name='Прочитано'),
        ),
    ]