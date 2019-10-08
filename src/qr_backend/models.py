from django.db import models


class Order(models.Model):
    order_id = models.CharField(max_length=12)
    paid = models.BooleanField(default=False)
    subtotal = models.DecimalField(null=True, decimal_places=2)
    tip = models.DecimalField(null=True, decimal_places=2)
    total = models.DecimalField(null=True, decimal_places=2)
