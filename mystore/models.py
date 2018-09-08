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

class Contact(models.Model):
    name = models.CharField(max_length = 264, blank = False)
    phone = models.CharField(max_length = 20)
    email = models.EmailField(blank = False)
    message = models.TextField()

    def __str__(self):
        return self.name

    class Meta:
        db_table = u'Contact'