# Generated by Django 4.1.7 on 2023-04-22 10:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reviews', '0002_alter_review_review_rating_alter_review_review_text'),
    ]

    operations = [
        migrations.AlterField(
            model_name='review',
            name='review_rating',
            field=models.IntegerField(choices=[(1, 1), (2, 2), (3, 3), (4, 4), (5, 5)], default=5, verbose_name='Оцінка'),
        ),
    ]
