from django.http import Http404
from django.utils.timezone import now
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, generics
from .models import Events, Tickets, Reservations
from .serializer import EventDetailSerializer, TicketListSerializer, ReservationSerializer, ReservationStatisticsSerializer
from .utils import PaymentGateway
import json


class EventDetail(APIView):
    def get(self, request, pk,format=None):
        try:
            event = Events.objects.get(pk=pk)
        except Event.DoesNotExist:
            raise Http404
        serializer = EventDetailSerializer(event)
        return Response(serializer.data)


class TicketList(generics.ListAPIView):
    serializer_class = TicketListSerializer
    queryset = Tickets.objects.all()


class ReservationList(generics.CreateAPIView):
    serializer_class = ReservationSerializer
    queryset = Reservations.objects.all()

class Payment(APIView):
    def post(self, request, format=None):
        data = json.loads(request.body.decode())
        p = PaymentGateway()
        try:
            r = Reservations.objects.get(pk=data['ticket'])
            price = r.ticket.price
            if price > data['amount']:
                return Respons({'error':'amount not sufficient'}, status=status.HTTP_400_BAD_REQUEST)
            if p.charge(amount=data['amount'], token=data['token']):
                r.payment_time = now()
                r.save()
                return Response(status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': "Error with payment"}, status=status.HTTP_400_BAD_REQUEST)
        

class ReservationDetail(APIView):
    def get(self, request, format=None):
        try:
            event = Reservations.objects.get(pk=pk)
        except Event.DoesNotExist:
            raise Http404
        serializer = EventDetailSerializer(event)
        return Response(serializer.data)
    

class ReservationStatistics(generics.ListAPIView):
    serializer_class = ReservationStatisticsSerializer
    queryset = Events.objects.all()