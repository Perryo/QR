from django.http import HttpResponse
from django.views.decorators.http import require_GET
from payment_app.controllers import order_controller
from django.template import loader
from django.views.decorators.csrf import csrf_exempt


@require_GET
def index(request):
    template = loader.get_template('index.html')
    return HttpResponse(template.render())


@csrf_exempt
def applepay_charge(request):
    return order_controller.handle_apply_pay_charge(request)


def stripe_charge(request):
    return order_controller.handle_stripe_charge(request)


def paypal_charge(request):
    return order_controller.handle_paypal_charge(request)


@require_GET
def order(request, order_id):
    return order_controller.handle_order(request, order_id)


@csrf_exempt
def survey(request):
    return order_controller.handle_survey(request)


@require_GET
def dashboard(request):
    return order_controller.dashboard(request)
