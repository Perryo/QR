import os

from django.apps import AppConfig
import json

with open(os.path.join('resources', 'credentials.json')) as json_file:
    data = json.load(json_file)
    STRIPE_API_KEY = data.get('stripe').get('api_key')
    PAYPAL_CLIENT_ID = data.get('paypal').get('client_id')
    PAYPAL_CLIENT_SECRET = data.get('paypal').get('client_secret')

class PaymentAppConfig(AppConfig):
    name = 'payment_app'
