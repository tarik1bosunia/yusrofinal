from django.db import models
from account.models import CustomUser
from store.models import Product


class Payment(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    payment_id = models.CharField(max_length=100)
    payment_method = models.CharField(max_length=100)
    amount_paid = models.CharField(max_length=100)  # this is the total amount paid
    status = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.payment_id


class Division(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class City(models.Model):
    name = models.CharField(max_length=50)
    division = models.ForeignKey(Division, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class Area(models.Model):
    name = models.CharField(max_length=100)
    city = models.ForeignKey('City', on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class Order(models.Model):
    STATUS = {
        ('New', 'New'),
        ("Accepted", "Accepted"),
        ("Completed", "Completed"),
        ("Cancelled", "Cancelled")
    }
    user = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True, blank=True)
    payment = models.ForeignKey(Payment, on_delete=models.SET_NULL, null=True, blank=True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    division = models.ForeignKey('Division', on_delete=models.CASCADE)
    city = models.ForeignKey('City', on_delete=models.CASCADE)
    area = models.ForeignKey('Area', on_delete=models.CASCADE)
    # delivery_type = models.CharField(max_length=50)
    address_line_1 = models.CharField(max_length=250)
    address_line_2 = models.CharField(max_length=250, blank=True)
    order_note = models.TextField(blank=True)
    order_total = models.IntegerField()
    discount = models.IntegerField()
    status = models.CharField(max_length=10, choices=STATUS, default="New")
    ip = models.CharField(max_length=20, blank=True)
    is_ordered = models.BooleanField(default=False)
    order_number = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def get_full_name(self):
        return f'{self.first_name} {self.last_name}'

    def get_full_address(self):
        return f'{self.address_line_1} {self.address_line_2}'

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class OrderProduct(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    Payment = models.ForeignKey(Payment, on_delete=models.SET_NULL, null=True, blank=True)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    # variation = models.ForeignKey(Variation, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    product_price = models.IntegerField()
    is_ordered = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def is_already_ordered(self):
        return OrderProduct.objects.filter(user=self.user, product=self.product, is_ordered=True).exists()
