# Generated by Django 4.1.7 on 2023-04-06 10:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_remove_doctor_email_doctor_category_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='doctor',
            name='profile_image',
            field=models.ImageField(blank=True, default='../media/default_image.png', upload_to=''),
        ),
    ]
