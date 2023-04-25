# Generated by Django 4.1.7 on 2023-04-21 15:08

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('users', '0003_alter_appointment_status'),
    ]

    operations = [
        migrations.CreateModel(
            name='Notification',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100, verbose_name='Заголовок сповіщення')),
                ('text', models.CharField(max_length=150, verbose_name='Текст сповіщення')),
                ('is_read', models.BooleanField(default=False, verbose_name='Прочитано: ')),
                ('patient', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='notification', to='users.patient')),
            ],
        ),
    ]