from collections import Counter
from datetime import datetime
import decimal

from django.db import models
from django.conf import settings


# Create your models here.
class Schedule(models.Model):
    schedule_no = models.CharField(max_length=32, unique=True)
    departure_time = models.DateTimeField()

    stations = models.ManyToManyField(to="Station", through="ScheduleToStation")
    carriages = models.ManyToManyField(to="Carriage", through="ScheduleToCarriage")

    def add_stations(self, station_ids, arrival_times):
        for i in range(len(station_ids)):
            station_id = station_ids[i]
            arrival_time = datetime.fromisoformat(arrival_times[i])

            schedule2station = ScheduleToStation(
                schedule=self,
                station_id=station_id,
                order=i,
                arrival_time=arrival_time,
            )
            schedule2station.save()

    def add_carriages(self, carriage_ids):
        carriage_count = Counter(carriage_ids)
        for carriage_id in carriage_count:
            num = carriage_count[carriage_id]

            schedule2carriage = ScheduleToCarriage(
                schedule=self,
                carriage_id=carriage_id,
                num=num,
            )
            schedule2carriage.save()

    def is_option_schedule(self, obj):
        self_first = self.scheduletostation_set.first().station
        self_last = self.scheduletostation_set.last().station
        obj_first = obj.scheduletostation_set.first().station
        obj_last = obj.scheduletostation_set.last().station
        return (obj != self) and self_first == obj_first and self_last == obj_last


class Station(models.Model):
    station_no = models.CharField(max_length=32, unique=True)
    name = models.CharField(max_length=32)


class ScheduleToStation(models.Model):
    schedule = models.ForeignKey(to="Schedule", on_delete=models.CASCADE)
    station = models.ForeignKey(to="Station", on_delete=models.CASCADE)
    order = models.IntegerField()
    arrival_time = models.DateTimeField()

    class Meta:
        ordering = ['order']


class Carriage(models.Model):
    name = models.CharField(max_length=32)
    seat_num = models.IntegerField()
    increase_rate = models.DecimalField(max_digits=10, decimal_places=2, default=1)


class ScheduleToCarriage(models.Model):
    schedule = models.ForeignKey(to="Schedule", on_delete=models.CASCADE)
    carriage = models.ForeignKey(to="Carriage", on_delete=models.CASCADE)
    num = models.IntegerField()

    def calc_cost(self):
        station_num = self.schedule.stations.count()
        carriage_increase_rate = self.carriage.increase_rate

        return (decimal.Decimal(carriage_increase_rate) * (
            (decimal.Decimal(station_num) - 1) *
            settings.AVG_KM_BETWEEN_STATION *
            settings.ADDITION_COST_PER_KM
        )).quantize(decimal.Decimal('0.00'))
    
    def get_seat_info(self):
        schedule2carriage = ScheduleToCarriage.objects.get(schedule=self.schedule, carriage=self.carriage)
        max_seat = schedule2carriage.num * schedule2carriage.carriage.seat_num
        now_seat = self.schedule.tickets.filter(carriage=self.carriage).count()

        return max_seat, now_seat

