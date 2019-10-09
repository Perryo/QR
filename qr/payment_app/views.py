from django.http import HttpResponse
from django.views.decorators.http import require_GET
from payment_app.controllers import order_controller


@require_GET
def order(request, order_id):
    return order_controller.handle_order(request, order_id)
