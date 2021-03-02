from django.urls import path, include

urlpatterns = [
    path('', include("ticket_system.urls")) 
]
