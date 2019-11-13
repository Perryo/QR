from django.http import HttpResponse
from django.views.decorators.http import require_GET
from payment_app.controllers import order_controller
from django.template import loader


@require_GET
def index(request):
    template = loader.get_template('index.html')
    return HttpResponse(template.render())


def charge(request):
    return order_controller.handle_charge(request)


@require_GET
def order(request, order_id):
    return order_controller.handle_order(request, order_id)


@require_GET
def dashboard(request):
    return order_controller.dashboard(request)
