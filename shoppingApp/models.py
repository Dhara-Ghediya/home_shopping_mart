from django.db import models

# Create your models here.
class User(models.Model):
    username = models.CharField(max_length=100, unique=True)
    password = models.CharField(max_length=50)
    email = models.EmailField(max_length=100, unique=True)
    phone = models.IntegerField()
    
    def __str__(self):
        return self.username
    
    class Meta:
        verbose_name = "User Record"
        
class Products(models.Model):
    Product_name = models.CharField(max_length=200)
    product_type = models.CharField(max_length=100)
    product_img = models.ImageField(upload_to='images')
    rating = models.IntegerField(default=0)
    description = models.TextField(max_length=500)
    price = models.FloatField()
    discount_amount = models.FloatField(default=0)
    
    def __str__(self):
        return self.Product_name
    
    class Meta:
        verbose_name = "Products Record"
        # ordering = [:-1]
        # db_table = 'X'
        get_latest_by = "Product_name"
    
class AddToCart(models.Model):
    user = models.CharField(max_length=100)
    product = models.ForeignKey(Products, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    
    class Meta:
        verbose_name = "Cart Record"
    
    