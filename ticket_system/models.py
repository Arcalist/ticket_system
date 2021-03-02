from django.db import models
from django.utils.timezone import now

# Create your models here.
class Reservations(models.Model):
    ticket = models.ForeignKey("Tickets", on_delete=models.CASCADE)
    reservation_time = models.DateTimeField(auto_now=True)
    payment_time = models.DateTimeField(null=True)

    def save(self, *args, **kwargs):
        if self.ticket.remaining_tickets() > 0 and self.ticket.event.start > now():
            super(Reservations, self).save(*args, **kwargs)

class Tickets(models.Model):
    event = models.ForeignKey("Events", on_delete=models.CASCADE)
    ticket_type = models.CharField(max_length=50)
    stock = models.IntegerField()
    price = models.FloatField()

    def sold_tickets(self):
        count = Reservations.objects.filter(ticket=self).count()
        return count

    def remaining_tickets(self):
        return self.stock - self.sold_tickets()

class Events(models.Model):
    name = models.CharField(max_length=100)
    start = models.DateTimeField()

    def ticket_types(self):
        types = Tickets.objects.filter(event=self).values_list('ticket_type', flat=True)
        return types

    def ticket_details(self):
        tickets = Tickets.objects.filter(event=self)
        ticket_list = []
        for t in tickets:
            ticket_list.append({'ticket_type': t.ticket_type,'remaining_tickets': t.remaining_tickets()})
        return ticket_list
    