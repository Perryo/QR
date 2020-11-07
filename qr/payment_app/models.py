from django.db import models
from django.utils import timezone


class Customer(models.Model):
    first_name = models.CharField(max_length=120, null=True)
    last_name = models.CharField(max_length=120, null=True)
    phone_number = models.CharField(unique=True, max_length=15, null=True)
    email_address = models.CharField(unique=True, max_length=50, null=True)
    would_use_qr = models.BooleanField(null=True)

    def __str__(self):
        if self.email_address:
            return self.email_address
        elif self.phone_number:
            return self.phone_number
        else:
            return '{}'.format(self.pk)


class Order(models.Model):
    # TODO: Add stripe and paypal order ids
    date = models.DateField(default=timezone.now)
    order_id = models.CharField(max_length=12)
    paid = models.BooleanField(default=False)
    subtotal = models.DecimalField(null=True, decimal_places=2, max_digits=7)
    tip = models.DecimalField(null=True, decimal_places=2, max_digits=7, default=0)
    total = models.DecimalField(null=True, decimal_places=2, max_digits=7, default=0)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return self.order_id
