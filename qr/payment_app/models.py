from django.db import models


class Order(models.Model):
    # TODO: Add stripe and paypal order ids
    order_id = models.CharField(max_length=12)
    paid = models.BooleanField(default=False)
    subtotal = models.DecimalField(null=True, decimal_places=2, max_digits=7)
    tip = models.DecimalField(null=True, decimal_places=2, max_digits=7, default=0)
    total = models.DecimalField(null=True, decimal_places=2, max_digits=7, default=0)

    def __str__(self):
        return self.order_id
