from django.http import HttpResponse
from django.template import loader
from django.core import serializers
import json
from payment_app.models import Order


def handle_order(self, order_id):
    # TODO: Look up the order
    order = Order.objects.get(order_id=order_id)
    # TODO: Check if the order is paid
    data = json.loads(serializers.serialize("json", [order]))[0]
    # TODO: Send price data to view

    # TODO: Return view
    template = loader.get_template('order_template.html')
    return HttpResponse(template.render(data))
