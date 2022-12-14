# Generated by Django 3.0.2 on 2020-02-25 16:46

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Recipe',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('mealName', models.CharField(max_length=50, verbose_name='Meal Name')),
                ('mealPic', models.ImageField(upload_to=None)),
                ('mealCookTime', models.IntegerField(blank=True, verbose_name='Cooking Time')),
                ('mealCalories', models.IntegerField(blank=True, verbose_name='Calories')),
                ('mealIngredients', models.CharField(max_length=100, verbose_name='Ingredient')),
                ('mealDirections', models.TextField(blank=True)),
                ('mealRate', models.IntegerField(blank=True)),
                ('mealComments', models.TextField(blank=True)),
            ],
        ),
    ]
