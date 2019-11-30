from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('applepay/charge', views.applepay_charge, name='applepay_charge'),
    path('stripe/charge', views.stripe_charge, name='stripe_charge'),
    path('paypal/charge', views.paypal_charge, name='paypal_charge'),
    path('order/<int:order_id>', views.order, name='order'),
    path('survey', views.survey, name='survey'),
    path('dashboard', views.dashboard, name='dashboard'),
]