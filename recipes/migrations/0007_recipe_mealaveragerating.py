# Generated by Django 3.0.3 on 2020-03-06 08:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0006_auto_20200228_1832'),
    ]

    operations = [
        migrations.AddField(
            model_name='recipe',
            name='mealAverageRating',
            field=models.PositiveIntegerField(default=1, verbose_name='Meal average rating'),
        ),
    ]
