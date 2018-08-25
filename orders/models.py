from django.db import models
from mystore.models import Product

# Create your models here.
 class Order(models.Model):
     first_name = models.CharField(max_length = 50)
     last_name = models.CharField(max_length = 50)
     email = models.EmailField()
     address = models.CharField(max_length = 250)
     postal_code = models.CharField(max_length = 20)
     city = models.CharField(max_length = 100)
     created = models.DateTimeField(auto_now= True)
     updateted = models.DateTimeField(auto_now= True)
     paid = models.BooleanField(default = False)

     class Meta:
         ordering = ('-created',)

    def __str__(self):
        return 'Order{}'.format(self.id)

    def get_total_cost(self):
        return sum(item.get_cost() for item in self.item.all())

class OrderItem(models.Model)