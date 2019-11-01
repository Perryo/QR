from django.urls import path

from . import views

urlpatterns = [
    path('order/<int:order_id>', views.order, name='order'),
    path('dashboard', views.dashboard, name='dashboard'),
]