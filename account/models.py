from django.db import models

# Create your models here.
import uuid

def generate_app_secret_token():
    return str(uuid.uuid4())

class Account(models.Model):
    email = models.EmailField(unique=True)
    account_id = models.CharField(max_length=255, unique=True)
    account_name = models.CharField(max_length=255)
    app_secret_token = models.CharField(max_length=255, default=generate_app_secret_token)
    website = models.URLField(blank=True, null=True)

class Destination(models.Model):
    account = models.ForeignKey(Account, on_delete=models.CASCADE)
    url = models.URLField()
    http_method = models.CharField(max_length=10)
    headers = models.JSONField()