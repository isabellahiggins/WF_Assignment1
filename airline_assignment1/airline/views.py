from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Flight, Booking, Invoice, Passenger
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User

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

def loginUser(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('index')
        else:
            return render(request, 'airline/login.html', {'error': 'Invalid username or password'})
    return render(request, 'airline/login.html')

def registerUser(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        name = request.POST['name'] 
        passportNum = request.POST['passport_number']
        phoneNum = request.POST['phone']
        #if username already exists
        if User.objects.filter(username=username).exists():
            return render(request, 'airline/register.html', {'error': 'Username already exists'})
        user = User.objects.create_user(username=username, password=password)
        #create passenger profile for the user
        Passenger.objects.create(user=user)
        login(request, user)
        return redirect('login')
    return render(request, 'airline/register.html')

def logoutUser(request):
    logout(request)
    return redirect('index')

def book_a_flight(request, flight_id):
    flight = Flight.objects.get(id=flight_id)
    if request.method == 'POST':
        passenger = Passenger.objects.get(user=request.user)
        booking = Booking.objects.create(
            flight=flight,
            passenger=passenger,
            status='confirmed',
            seat_class=request.POST['seat_class']
        )
        return redirect('bookings')
    return render(request, 'airline/book_a_flight.html', {'flight': flight})