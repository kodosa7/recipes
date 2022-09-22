from django.db import models
from datetime import datetime
from django.utils import timezone
from django.urls import reverse
from datetime import datetime
import requests

# Create your models here.
class Recipe(models.Model):
    # we have several models in db
    mealName = models.CharField(max_length=50, verbose_name=('Meal Name'))
    mealPic = models.ImageField(upload_to=(''), max_length=100, verbose_name=('Meal Image'))
    mealCookTime = models.PositiveIntegerField(default=1, verbose_name=('Cooking Time'))
    mealCalories = models.PositiveIntegerField(default=1, verbose_name=('Calories'))
    mealIngredient1 = models.CharField(blank=True, max_length=100, verbose_name=('Ingredient #1'))
    mealIngredient2 = models.CharField(blank=True, max_length=100, verbose_name=('Ingredient #2'))
    mealIngredient3 = models.CharField(blank=True, max_length=100, verbose_name=('Ingredient #3'))
    mealIngredient4 = models.CharField(blank=True, max_length=100, verbose_name=('Ingredient #4'))
    mealIngredient5 = models.CharField(blank=True, max_length=100, verbose_name=('Ingredient #5'))
    mealIngredient6 = models.CharField(blank=True, max_length=100, verbose_name=('Ingredient #6'))
    mealIngredient7 = models.CharField(blank=True, max_length=100, verbose_name=('Ingredient #7'))
    mealIngredient8 = models.CharField(blank=True, max_length=100, verbose_name=('Ingredient #8'))
    mealIngredient9 = models.CharField(blank=True, max_length=100, verbose_name=('Ingredient #9'))
    mealIngredient10 = models.CharField(blank=True, max_length=100, verbose_name=('Ingredient #10'))
    mealDirection1 = models.TextField(blank=True, max_length=500, verbose_name=('Direction #1'))
    mealDirection2 = models.TextField(blank=True, max_length=500, verbose_name=('Direction #2'))
    mealDirection3 = models.TextField(blank=True, max_length=500, verbose_name=('Direction #3'))
    mealDirection4 = models.TextField(blank=True, max_length=500, verbose_name=('Direction #4'))
    mealDirection5 = models.TextField(blank=True, max_length=500, verbose_name=('Direction #5'))

    mealIP = models.CharField(blank=True, max_length=16, verbose_name=('user IP address'))
    mealDbRating = models.PositiveIntegerField(default=1, verbose_name=('Meal rating'))
    mealAverageRating = models.PositiveIntegerField(default=1, verbose_name=('Meal average rating'))

    class Meta:
        verbose_name_plural = 'oxen'

    # get recipe url by id for use in templates
    def getRecipeUrl(self):
        return reverse('recipe_detail_view', kwargs={'id': self.id})

    def __str__(self):
        return self.mealName
