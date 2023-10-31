from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Recipe(models.Model):
  name = models.CharField(max_length=120)
  ingredients = models.CharField(max_length=250)
  cooking_time = models.IntegerField(help_text='in minutes')
  description = models.TextField()
  pic = models.ImageField(upload_to='recipes', default='no_image.svg')
  # created_by = models.ForeignKey(User, on_delete=models.CASCADE)
  create_on = models.DateTimeField(auto_now_add=True)
  
  # calculate difficulty based on cooking time and number of ingredients
  def calculate_difficulty(self):
    num_ingredients = len(self.ingredients.split(', '))
    if self.cooking_time < 10 and num_ingredients < 4:
      difficulty = 'Easy'
    elif self.cooking_time < 10 and num_ingredients >= 4:
      difficulty = 'Medium'
    elif self.cooking_time >= 10 and num_ingredients < 4:
      difficulty = 'Intermediate'
    elif self.cooking_time >= 10 and num_ingredients >=4:
      difficulty = 'Hard'
    return difficulty
  
  def __str__(self):
    return str(self.name)