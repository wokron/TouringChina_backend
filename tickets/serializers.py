from rest_framework import serializers

from schedules.models import Carriage, Schedule
from tickets.models import Ticket


class CarriageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Carriage
        fields = ['id', 'name']


class ScheduleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Schedule
        fields = ['id', 'schedule_no', 'departure_time']


class TicketSerializer(serializers.ModelSerializer):
    is_expired = serializers.SerializerMethodField()
    schedule = ScheduleSerializer()
    carriage = CarriageSerializer()

    class Meta:
        model = Ticket
        fields = "__all__"
        exclude = ['user']

    def get_is_expired(self, obj):
        return obj.is_expire()
