from django.contrib import admin
from .models import *

# Register your models here.
class UserAdmin(admin.ModelAdmin):
    list_display = ["username", "email", "phone"]
admin.site.register(User, UserAdmin)

class ProductsAdmin(admin.ModelAdmin):
    list_display = ['Product_name', 'product_type', 'price', 'discount_amount']
admin.site.register(Products, ProductsAdmin)

class AddToCartAdmin(admin.ModelAdmin):
    list_display = ["user", "product", "quantity"]
admin.site.register(AddToCart, AddToCartAdmin)