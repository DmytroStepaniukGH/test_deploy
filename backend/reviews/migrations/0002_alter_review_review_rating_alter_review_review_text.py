# Generated by Django 4.1.7 on 2023-04-22 09:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reviews', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='review',
            name='review_rating',
            field=models.IntegerField(choices=[(0, 0), (1, 1), (2, 2), (3, 3), (4, 4), (5, 5)], default=0, verbose_name='Оцінка'),
        ),
        migrations.AlterField(
            model_name='review',
            name='review_text',
            field=models.CharField(max_length=2000, verbose_name='Відгук'),
        ),
    ]
