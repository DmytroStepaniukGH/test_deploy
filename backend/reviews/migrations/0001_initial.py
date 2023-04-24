# Generated by Django 4.1.7 on 2023-04-17 15:47

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Review',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('review_rating', models.FloatField(default=0)),
                ('review_text', models.CharField(max_length=2000)),
                ('appointment', models.OneToOneField(default=1, on_delete=django.db.models.deletion.CASCADE, to='users.appointment')),
                ('doctor', models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='users.doctor')),
            ],
        ),
    ]
