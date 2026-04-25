from django.shortcuts import render
from django.http import HttpResponse
from .models import Flight, Booking, Invoice

# Create your views here.
def index(request):
    flights = Flight.objects.all()
    return render(request, 'airline/index.html', {'flights': flights})

def flight_detail(request, flight_id):
    flight = Flight.objects.get(id=flight_id)
    return render(request, 'airline/flight_detail.html', {'flight': flight})

def book_a_flight(request, flight_id):
    flight = Flight.objects.get(id=flight_id)
    return render(request, 'airline/book_a_flight.html', {'flight': flight})

def bookings(request):
    bookings = Booking.objects.all()
    return render(request, 'airline/bookings.html', {'bookings': bookings})

def invoices(request):
    invoices = Invoice.objects.all()
    return render(request, 'airline/invoices.html', {'invoices': invoices})