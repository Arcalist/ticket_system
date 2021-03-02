from rest_framework import serializers
from .models import Tickets, Events, Reservations


class EventDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Events
        fields = ['id', 'name', 'start', 'ticket_types']


class TicketListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tickets
        fields = ['id', 'event', 'ticket_type', 'stock', 'price', 'remaining_tickets']
        read_only_fields = ['remaining_tickets']


class ReservationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reservations
        fields = ['id', 'ticket', 'reservation_time', 'payment_time', 'payed']
        read_only_fields = ['reservation_time', 'payment_time', 'payed']


class ReservationStatisticsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Events
        fields = ['id', 'name', 'ticket_details']

