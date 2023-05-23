from django.db import models
from store.models import Product, Variation
from account.models import CustomUser


# Create your models here.

class Cart(models.Model):
    cart_id = models.CharField(max_length=250, blank=True)
    date_added = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.cart_id


class CartItem(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    variations = models.ManyToManyField(Variation, blank=True)
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, null=True)
    quantity = models.IntegerField()
    is_active = models.BooleanField(default=True)

    def sub_total(self):
        return self.product.selling_price * self.quantity

    def __unicode__(self):
        return self.product


# class Division(models.Model):
#     name = models.CharField(max_length=50)
#
#     def __str__(self):
#         return self.name
#
#
# class City(models.Model):
#     name = models.CharField(max_length=50)
#     division = models.ForeignKey(Division, on_delete=models.CASCADE)
#
#     def __str__(self):
#         return self.name
#
#
# class Area(models.Model):
#     name = models.CharField(max_length=100)
#     city = models.ForeignKey('City', on_delete=models.CASCADE)
#
#     def __str__(self):
#         return self.name
#
#
# class Order(models.Model):
#     user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=True, blank=True)
#     first_name = models.CharField(max_length=100)
#     last_name = models.CharField(max_length=100)
#     email = models.EmailField()
#     phone = models.CharField(max_length=20)
#     division = models.ForeignKey('Division', on_delete=models.CASCADE)
#     city = models.ForeignKey('City', on_delete=models.CASCADE)
#     area = models.ForeignKey('Area', on_delete=models.CASCADE)
#     delivery_type = models.CharField(max_length=50)
#     address_1 = models.CharField(max_length=250)
#     address_2 = models.CharField(max_length=250, blank=True)
#     note = models.TextField(blank=True)
#     created_at = models.DateTimeField(auto_now_add=True)
#
#     def __str__(self):
#         return f"{self.first_name} {self.last_name}"

