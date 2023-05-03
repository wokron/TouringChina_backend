from django.contrib.auth.models import User
from django.db import models


# Create your models here.
class Account(models.Model):
    card_id = models.CharField(max_length=32)

    user = models.ForeignKey(to=User, on_delete=models.CASCADE)
