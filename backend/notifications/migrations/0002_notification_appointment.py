# Generated by Django 4.1.7 on 2023-04-25 16:47

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0005_remove_appointment_is_confirmed_and_more'),
        ('notifications', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='notification',
            name='appointment',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='appointment', to='users.appointment'),
            preserve_default=False,
        ),
    ]
