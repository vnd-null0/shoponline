from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Product(models.Model):
    name = models.CharField(max_length=264,unique=True)
    fee = models.IntegerField()
    description = models.TextField()
    image = models.ImageField(upload_to = "images/")

    def __str__(self):
        return str(self.name)