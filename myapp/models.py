from django.db import models
from django.utils import timezone


class MyUser(models.Model):
    USER_TYPES = (
        ('employee', 'Employee'),
        ('customer', 'Customer'),
    )

    username = models.CharField(max_length=50)
    password = models.CharField(max_length=50)
    user_type = models.CharField(max_length=10, choices=USER_TYPES)
    last_login = models.DateTimeField(default=timezone.now)

    class Meta:
        db_table = 'myapp_myuser'


class Employee(models.Model):
    username = models.ForeignKey(MyUser, on_delete=models.CASCADE)
    emp_name = models.CharField(max_length=255)
    active_orders_count = models.IntegerField(default=0)


class NewCustomerOrder(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    username = models.ForeignKey(MyUser, on_delete=models.CASCADE)
    customer_name = models.CharField(max_length=255)
    age = models.IntegerField()
    marital_status = models.CharField(max_length=50)
    phone_number = models.CharField(max_length=50)
    email = models.EmailField(max_length=50)
    status = models.CharField(max_length=50, default='waiting')
