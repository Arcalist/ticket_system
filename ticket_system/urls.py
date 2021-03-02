from django.urls import path

from . import views

urlpatterns = [
    path('event/<int:pk>/', views.EventDetail.as_view(), name='event'),
    path('tickets/', views.TicketList.as_view(), name='tickets'),
    path('payment/', views.Payment.as_view(), name='payment'),
    path('reservations/', views.ReservationList.as_view(), name='reservations'),
    path('reservations/<int:pk>/', views.ReservationDetail.as_view(), name='reservation-detail'),
    path('reservation_statistics/', views.ReservationStatistics.as_view(), name='reservation-statistics'),
]