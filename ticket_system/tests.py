from django.urls import reverse
from django.utils.timezone import now
from rest_framework import status
from rest_framework.test import APITestCase
from .models import Events, Tickets, Reservations
from .serializer import EventDetailSerializer
import datetime

class TicketsTestCase(APITestCase):

    def setUp(self):
        self.now = now()
        event1 = Events.objects.create(name="Event 1", start=self.now + datetime.timedelta(days=10))
        event2 = Events.objects.create(name="Event 2", start=self.now + datetime.timedelta(days=5))
        event3 = Events.objects.create(name="Event 3", start=self.now + datetime.timedelta(days=2))
        ticket11 = Tickets.objects.create(event=event1, ticket_type='VIP', stock=1000, price=1000)
        ticket12 = Tickets.objects.create(event=event1, ticket_type='Premium', stock=10000, price=500)
        ticket13 = Tickets.objects.create(event=event1, ticket_type='Normal', stock=40000, price=100)
        ticket21 = Tickets.objects.create(event=event2, ticket_type='Ticket1', stock=5000, price=200)
        ticket22 = Tickets.objects.create(event=event2, ticket_type='Ticket2', stock=5000, price=200)
        ticket3 = Tickets.objects.create(event=event3, ticket_type='Ticket', stock=100000, price=50)

    def test_get_event(self):
        """
        Testing getting info about events
        """
        url = reverse('event', kwargs={'pk': 1})
        event = EventDetailSerializer(Events.objects.get(pk=1))
        response = self.client.get(url)
        data = response.json()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data, {'id': 1, 'name': 'Event 1', 'start': event['start'].value, 'ticket_types': ['VIP', 'Premium', 'Normal']})


    def test_get_tickets_info(self):
        """
        Testing getting info about tickets
        """
        url = reverse('tickets')
        response = self.client.get(url)
        data = response.json()
        self.assertEqual(data[0], {'id': 1, 'event': 1, 'ticket_type': 'VIP', 'stock': 1000, 'price': 1000.0, 'remaining_tickets': 1000, 'sold_tickets': 0})
        self.assertEqual(data[1], {'id': 2, 'event': 1, 'ticket_type': 'Premium', 'stock': 10000, 'price': 500.0, 'remaining_tickets': 10000, 'sold_tickets': 0})
        self.assertEqual(data[2], {'id': 3, 'event': 1, 'ticket_type': 'Normal', 'stock': 40000, 'price': 100.0, 'remaining_tickets': 40000, 'sold_tickets': 0})
        self.assertEqual(data[3], {'id': 4, 'event': 2, 'ticket_type': 'Ticket1', 'stock': 5000, 'price': 200.0, 'remaining_tickets': 5000, 'sold_tickets': 0})
        self.assertEqual(data[4], {'id': 5, 'event': 2, 'ticket_type': 'Ticket2', 'stock': 5000, 'price': 200.0, 'remaining_tickets': 5000, 'sold_tickets': 0})
        self.assertEqual(data[5], {'id': 6, 'event': 3, 'ticket_type': 'Ticket', 'stock': 100000, 'price': 50.0, 'remaining_tickets': 100000, 'sold_tickets': 0})


    def test_reserve_ticket(self):
        """
        Testing reservation ticket
        """
        url = reverse('reservations')
        response = self.client.post(url, {'ticket': 1})
        self.assertEqual(Reservations.objects.all().count(), 1)

    def test_fail_to_reserve_sold_out(self):
        """
        Testing if you can reserve tickets when there are none
        """
        url = reverse('reservations')
        for x in range(0,2000):
            response = self.client.post(url, {'ticket': 1})
        self.assertEqual(Reservations.objects.all().count(), 1000)
    
    def test_payment(self):
        url = reverse('reservations')
        response = self.client.post(url, {'ticket': 1})
        self.assertEqual(Reservations.objects.all().count(), 1)
        url = reverse('payment')
        response = self.client.post(url, {'ticket': 1, 'amount': 1000, 'token': 'dssdgsdesdg'}, format='json')
        self.assertNotEqual(Reservations.objects.get(pk=1).payment_time, None)

    def test_error_payment(self):
        url = reverse('reservations')
        response = self.client.post(url, {'ticket': 1})
        self.assertEqual(Reservations.objects.all().count(), 1)
        url = reverse('payment')
        response = self.client.post(url, {'ticket': 1, 'amount': 1000, 'token': 'card_error'}, format='json')
        self.assertEqual(Reservations.objects.get(pk=1).payment_time, None)

    def test_reservation_statistics(self):
        url = reverse('reservation-statistics')
        response = self.client.get(url)
        data = response.json()
        print(data)
        self.assertEqual