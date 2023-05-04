from datetime import timedelta, datetime

from django.contrib.auth.models import User
from django.db import models

from schedules.models import Schedule, Carriage


# Create your models here.
class Ticket(models.Model):
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    create_time = models.DateTimeField(auto_now_add=True)
    is_paid = models.BooleanField(default=False)
    is_schedule_modified = models.BooleanField(default=False)
    seat_no = models.IntegerField()

    schedule = models.ForeignKey(to=Schedule, on_delete=models.SET_NULL)
    carriage = models.ForeignKey(to=Carriage, on_delete=models.CASCADE)
    user = models.ForeignKey(to=User, on_delete=models.CASCADE, related_name='tickets')

    def is_expired(self):
        return not self.is_paid and self.create_time + timedelta(days=1) > datetime.now()

    def is_deletable(self):
        return not self.is_paid or self.is_expired()

    def is_cancelable(self):
        return self.is_paid and datetime.now() + timedelta(hours=1) < self.schedule.departure_time
