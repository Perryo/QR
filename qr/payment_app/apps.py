import os

from django.apps import AppConfig
import json

with open(os.path.join('resources', 'credentials.json')) as json_file:
    data = json.load(json_file)
    STRIPE_API_KEY = data.get('stripe').get('api_key')


class PaymentAppConfig(AppConfig):
    name = 'payment_app'
