import stripe
from django.http import HttpResponse, HttpResponseBadRequest
from django.shortcuts import render_to_response
from django.template import loader, RequestContext
from django.core import serializers
import json

from payment_app import apps
from payment_app.controllers.paypal_client import GetOrder
from payment_app.models import Order
from decimal import Decimal


def handle_stripe_charge(request):
    if not stripe.api_key:
        stripe.api_key = apps.STRIPE_API_KEY
    # Token is created using Checkout or Elements!
    # Get the payment token ID submitted by the form:
    # TODO: Catch stripe.error.InvalidRequestError and reload page with same order info
    token = request.POST.get('stripeToken')
    order_id = request.POST.get('orderId')
    tip = request.POST.get('tip')
    try:
        tip = Decimal(tip)
    except TypeError:
        tip = Decimal(0)

    if token:
        order = Order.objects.get(order_id=order_id)
        stripe_total = str(order.subtotal + tip).replace('.', '')
        charge = stripe.Charge.create(
            amount=stripe_total,
            currency='usd',
            description='QR charge',
            source=token,
        )
        if not charge.failure_code:
            # Set order paid
            order.tip = tip
            order.total = order.subtotal + tip
            order.paid = True
            order.save()
            return build_order_template(order, 'paid.html')

    else:
        return HttpResponseBadRequest()


def handle_paypal_charge(request):
    # TODO: What is this? Docs recommend it
    # request = OrdersCreateRequest()
    # request.headers['PayPal-Partner-Attribution-Id'] = 'PARTNER_ID_ASSIGNED_BY_YOUR_PARTNER_MANAGER'
    qr_order_id = request.POST.get('qrOrderId')
    tip = request.POST.get('tip')
    paypal_order_id = request.POST.get('paypalOrderId')
    order = Order.objects.get(order_id=qr_order_id)
    response = GetOrder().get_order(paypal_order_id)
    if response.status_code == 200:
        if response.result.status == 'COMPLETED':
            order.paid = True
            order.tip = Decimal(tip)
            order.total = Decimal(response.result.purchase_units[0].amount.value)
            order.save()
            return build_order_template(order, 'paid.html')


def handle_order(request, order_id):
    order = Order.objects.get(order_id=order_id)
    # If order is already paid view will handle it
    return build_order_template(order, 'order_template.html')


def dashboard(request):
    context = RequestContext(request)
    orders = Order.objects.all()
    data = {'orders': orders}
    return render_to_response('dashboard.html', data, context)


def build_order_template(order, page):
    data = json.loads(serializers.serialize("json", [order]))[0]
    template = loader.get_template(page)
    return HttpResponse(template.render(data))
