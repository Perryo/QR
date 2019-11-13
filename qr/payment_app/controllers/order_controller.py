import stripe
from django.http import HttpResponse, HttpResponseBadRequest
from django.shortcuts import render_to_response
from django.template import loader, RequestContext
from django.core import serializers
import json
from payment_app.models import Order

stripe.api_key = 'sk_test_jk6W0zrSFSnM4AcsN4hp5vAH'

def handle_charge(request):
    # Token is created using Checkout or Elements!
    # Get the payment token ID submitted by the form:
    token = request.POST.get('stripeToken')
    order_id = request.POST.get('orderId')
    amount = request.POST.get('amount')

    if token:
        charge = stripe.Charge.create(
            amount=amount,
            currency='usd',
            description='QR charge',
            source=token,
        )
        if not charge.failure_code:
            # Set order paid
            order = Order.objects.get(order_id=order_id)
            order.paid = True
            order.save()
            return build_order_template(order)

    else:
        return HttpResponseBadRequest()


def handle_order(request, order_id):
    order = Order.objects.get(order_id=order_id)
    # If order is already paid view will handle it
    return build_order_template(order)


def dashboard(request):
    context = RequestContext(request)
    orders = Order.objects.all()
    data = {'orders': orders}
    return render_to_response('dashboard.html', data, context)


def build_order_template(order):
    data = json.loads(serializers.serialize("json", [order]))[0]
    template = loader.get_template('order_template.html')
    return HttpResponse(template.render(data))