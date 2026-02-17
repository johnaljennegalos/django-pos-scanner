from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Customer(models.Model):
    name = models.CharField(max_length=100, null=True)
    email = models.EmailField(max_length=100, null=True)
    address = models.CharField(max_length=100, null=True)
    phone = models.CharField(max_length=100, null=True)
    date_created = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return self.name

class Branch(models.Model):
    name = models.CharField(max_length=100, null=True)
    address = models.CharField(max_length=100, null=True)
    phone_number = models.CharField(max_length=100, null=True)

    def __str__(self):
        return self.name

class Employee(models.Model):
    ROLE_CHOICES = (
    ('Sales Agent', 'Sales Agent'),
    ('Credit Officer', 'Credit Officer'),
    ('Manager', 'Manager'),
    )

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    branch = models.ForeignKey(Branch, on_delete=models.CASCADE)
    name = models.CharField(max_length=100, null=True)
    role = models.CharField(choices=ROLE_CHOICES, max_length=100, null=True)
    hire_date = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.name

class Supplier(models.Model):
    name = models.CharField(max_length=100, null=True)
    contact_person = models.CharField(max_length=100, null=True)
    phone = models.CharField(max_length=100, null=True)

    def __str__(self):
        return self.name

class Product(models.Model):
    supplier = models.ForeignKey(Supplier, on_delete=models.CASCADE)
    product_name = models.CharField(max_length=100, null=True)
    base_price = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    barcode = models.CharField(max_length=100, null=True)

    def __str__(self):
        return f"{self.product_name} | {self.barcode}"
