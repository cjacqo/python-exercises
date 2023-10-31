from django.db import models
from django.contrib.auth.models import User #needed for OneToOneField

# Create your models here.
class User(models.Model):
  # username = models.OneToOneField(User, on_delete=models.CASCADE)
  name = models.CharField(max_length=50)

  def __str__(self):
    return str(self.name)