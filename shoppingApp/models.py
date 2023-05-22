from django.db import models

# Create your models here.
class User(models.Model):
    username = models.CharField(max_length=100, unique=True)
    password = models.CharField(max_length=50)
    email = models.EmailField(max_length=100, unique=True)
    phone = models.IntegerField()
    
class Products(models.Model):
    Product_name = models.CharField(max_length=200)
    product_type = models.CharField(max_length=100)
    product_img = models.ImageField(upload_to='images')
    rating = models.IntegerField(default=0)
    description = models.TextField(max_length=500)
    price = models.FloatField()
    
    def __str__(self):
        return self.Product_name
    
    