from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Customer(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(max_length=100, blank=True)
    address = models.CharField(max_length=100, blank=True)
    phone = models.CharField(max_length=100, blank=True)
    date_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class Branch(models.Model):
    name = models.CharField(max_length=100)
    address = models.CharField(max_length=100, blank=True)
    phone_number = models.CharField(max_length=100, blank=True)

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
    name = models.CharField(max_length=100)
    role = models.CharField(choices=ROLE_CHOICES, max_length=100, default='Sales Agent')
    hire_date = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.name

class Supplier(models.Model):
    name = models.CharField(max_length=100)
    contact_person = models.CharField(max_length=100, blank=True)
    phone = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return self.name

class Product(models.Model):
    supplier = models.ForeignKey(Supplier, on_delete=models.CASCADE)
    product_name = models.CharField(max_length=100)
    base_price = models.DecimalField(max_digits=10, decimal_places=2)
    barcode = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return f"{self.product_name} | {self.barcode}"

class BranchInventory(models.Model):
    branch = models.ForeignKey(Branch, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.branch} | {self.product} | {self.quantity}"

class Order(models.Model):
    ORDER_STATUS = (
    ('Pending', 'Pending'),
    ('Completed', 'Completed'),
    ('Cancelled', 'Cancelled'),
    )

    PAYMENT_METHOD = (
    ('CASH', 'CASH'),
    ('INSTALLMENT', 'INSTALLMENT'),
    )

    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True, blank=True)
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    branch = models.ForeignKey(Branch, on_delete=models.CASCADE)

    order_date = models.DateField(auto_now_add=True)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    order_status = models.CharField(choices=ORDER_STATUS, max_length=100, default='Pending')
    payment_method = models.CharField(choices=PAYMENT_METHOD, max_length=100)

    def __str__(self):
        return f"{self.id} | {self.branch.name}"


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    unit_price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.quantity} | {self.product.name}"

class Payment(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    amount_paid = models.DecimalField(max_digits=10, decimal_places=2)
    date_paid = models.DateTimeField(auto_now_add=True)
    payment_type = models.CharField(max_length=100, choices=Order.PAYMENT_METHOD)

    def __str__(self):
        return f"Payment for Order #{self.order.id}"

class CashPayment(models.Model):
    payment = models.OneToOneField(Payment, on_delete=models.CASCADE)
    cash_received = models.DecimalField(max_digits=10, decimal_places=2)
    change_given = models.DecimalField(max_digits=10, decimal_places=2)

class InstallmentPlan(models.Model):
    payment = models.OneToOneField(Payment, on_delete=models.CASCADE)
    term_months = models.IntegerField()
    monthly_due = models.DecimalField(max_digits=10, decimal_places=2)
    remaining_balance = models.DecimalField(max_digits=10, decimal_places=2)
    next_due_date = models.DateField()
    payment_status = models.CharField(max_length=100, choices=Order.ORDER_STATUS)

class Invoice(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    or_number = models.CharField(max_length=100, unique=True)
    invoice_date = models.DateTimeField(auto_now_add=True)
    vat_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    grand_total = models.DecimalField(max_digits=10, decimal_places=2)
    issued_by = models.ForeignKey(Employee, on_delete=models.CASCADE)

    def __str__(self):
        return f"Invoice {self.or_number}"
