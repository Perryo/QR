from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('charge', views.charge, name='charge'),
    path('order/<int:order_id>', views.order, name='order'),
    path('dashboard', views.dashboard, name='dashboard'),
]