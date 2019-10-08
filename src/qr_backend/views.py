from django.http import HttpResponse

from src.qr_backend.controllers import order_controller


def order(request, order_id):
    return order_controller.handle_order(request, order_id)
