import datetime

import stripe
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse, JsonResponse, HttpResponseNotFound
from django.shortcuts import render_to_response
from django.template import loader, RequestContext
from django.core import serializers
import json

from stripe.error import InvalidRequestError

from payment_app import apps
from payment_app.controllers.paypal_client import GetOrder
from payment_app.models import Order, Customer
from decimal import Decimal


# TODO: Gather email and for sending receipt?
# https://stripe.com/docs/receipts

def handle_apply_pay_charge(request):
    body = json.loads(request.body)
    token = body.get('stripeToken')
    order_id = body.get('orderId')
    tip = body.get('tip')
    order = Order.objects.get(order_id=order_id)
    if do_stripe_charge(token, order, tip):
        return JsonResponse({'success': 'true'})


def handle_stripe_charge(request):
    # Token is created using Checkout or Elements!
    # Get the payment token ID submitted by the form:
    token = request.POST.get('stripeToken')
    order_id = request.POST.get('orderId')
    tip = request.POST.get('tip')
    order = Order.objects.get(order_id=order_id)
    if do_stripe_charge(token, order, tip):
        return build_order_template(order, 'paid.html', request)
    else:
        return build_order_template(order, 'order_template.html', request)


def save_customer_info(order, email, phone, name):
    customer = None
    first_name = None
    last_name = None
    if name:
        name = name.split(' ', 1)
        first_name = name[0]
        if len(name) > 1:
            last_name = name[1]
    # Look up by email
    try:
        customer = Customer.objects.get(email_address=email)
    except ObjectDoesNotExist:
        try:
            # If not found lookup by phone number
            if phone and not customer:
                customer = Customer.objects.get(phone=phone)
        except ObjectDoesNotExist:
            pass
    # If this customer still hasnt been found create one
    if not customer:
        customer = Customer()
    # Set info that is missing
    customer.email_address = customer.email_address or email
    customer.phone_number = customer.phone_number or phone
    customer.first_name = customer.first_name or first_name
    customer.last_name = customer.last_name or last_name
    customer.save()
    order.customer = customer


# TODO: This should raise exceptions
def do_stripe_charge(token, order, tip):
    if order.paid:
        return True
    if not stripe.api_key:
        stripe.api_key = apps.STRIPE_API_KEY
    try:
        tip = Decimal(tip)
    except TypeError:
        tip = Decimal(0)
    if token:
        try:
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
                if charge.billing_details:
                    customer = charge.billing_details
                    save_customer_info(order, customer.email, customer.phone, customer.name)
                order.save()
                return True
        except InvalidRequestError:
            return False
    else:
        return False


def handle_paypal_charge(request):
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
            try:
                customer = response.result.payer
                name = '{} {}'.format(customer.name.given_name, customer.name.surname)
                save_customer_info(order, customer.email_address, None, name)
            except Exception:
                pass
            order.save()
            return build_order_template(order, 'paid.html', request)


def handle_order(request, order_id):
    try:
        order = Order.objects.get(order_id=order_id)
    except ObjectDoesNotExist:
        return HttpResponseNotFound()
    # If order is already paid view will handle it
    if order.paid:
        return build_order_template(order, 'paid.html', request)
    else:
        return build_order_template(order, 'order_template.html', request)


def dashboard(request):
    context = RequestContext(request)
    orders = Order.objects.all()
    data = {'orders': orders}
    return render_to_response('dashboard.html', data, context)


def build_order_template(order, page, request):
    data = json.loads(serializers.serialize("json", [order]))[0]
    date = data['fields'].get('date')
    if date:
        formatted_date = datetime.datetime.strptime(date, '%Y-%m-%d').strftime('%b %d %Y')
        data['fields']['date'] = formatted_date
    template = loader.get_template(page)
    return HttpResponse(template.render(data, request))


def handle_survey(request):
    body = json.loads(request.body)
    order_id = body.get('orderId')
    would_use = body.get('wouldUse')
    order = Order.objects.get(order_id=order_id)
    customer = order.customer
    customer.would_use_qr = would_use == 'true'
    customer.save()
    return HttpResponse(200)
