from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Flight, Booking, Invoice, Passenger
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required   

# Create your views here.
@login_required
def index(request):
    flights = Flight.objects.all()
    return render(request, 'airline/index.html', {'flights': flights})

@login_required
def flight_detail(request, flight_id):
    flight = Flight.objects.get(id=flight_id)
    return render(request, 'airline/flight_detail.html', {'flight': flight})

@login_required
def bookings(request):
    if request.user.is_staff or request.user.groups.filter(name='Travel Agent').exists():
        bookings = Booking.objects.all()
    else:
        passenger = Passenger.objects.get(user=request.user)
        bookings = Booking.objects.filter(passenger=passenger)
    return render(request, 'airline/bookings.html', {'bookings': bookings})

@login_required
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
        Passenger.objects.create(
            user=user,
            name=name,
            passport_number=passportNum,
            phone=phoneNum
        )
        login(request, user)
        return redirect('login')
    return render(request, 'airline/register.html')

def logoutUser(request):
    logout(request)
    return redirect('index')

@login_required
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
        
        Invoice.objects.create(
                booking=booking,
                total=flight.price,
                status='unpaid'
            )
        return redirect('bookings')
    return render(request, 'airline/book_a_flight.html', {'flight': flight})

@login_required
def passengers(request):
    if not request.user.is_staff and not request.user.groups.filter(name='Travel Agent').exists():
        return redirect('index')
    passengers = Passenger.objects.all()
    return render(request, 'airline/passengers.html', {'passengers': passengers})

@login_required
def cancelBooking(request, booking_id):
    if not request.user.groups.filter(name='Travel Agent').exists():
        return redirect('index')
    booking = Booking.objects.get(id=booking_id)
    booking.status = 'cancelled'
    booking.save()
    return redirect('bookings')


