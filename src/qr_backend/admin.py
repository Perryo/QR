from django.contrib import admin

# Register your models here.
from src.qr_backend import models

admin.register(models.Order)