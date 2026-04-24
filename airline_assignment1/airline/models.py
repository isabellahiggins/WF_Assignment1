from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Flight(models.Model):
    flight_number = models.CharField(max_length=5)
    departure = models.CharField(max_length=50)
    destination = models.CharField(max_length=50)
    departure_time = models.DateTimeField()
    arrival_time = models.DateTimeField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    
    def __str__(self):
        return f"flight number: {self.flight_number}, departure: {self.departure}, destination: {self.destination}"

class Passenger(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100) 
    passport_number = models.CharField(max_length=20)
    phone = models.CharField(max_length=20)

    def __str__(self):
        return self.name

class Booking(models.Model):
    STATUS = [
        ('confirmed', 'Confirmed'),
        ('cancelled', 'Cancelled'),
    ]

    passenger = models.ForeignKey(Passenger, on_delete=models.CASCADE)
    flight = models.ForeignKey(Flight, on_delete=models.CASCADE)
    seat_class = models.CharField(max_length=20, default='economy')
    status = models.CharField(max_length=20, choices=STATUS, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Booking {self.id} - {self.passenger} on {self.flight}"

class Invoice(models.Model):
    booking = models.OneToOneField(Booking, on_delete=models.CASCADE)
    issued_date = models.DateTimeField(auto_now_add=True)
    total = models.DecimalField(max_digits=8, decimal_places=2)
    status = models.CharField(max_length=20, default='unpaid')

    def __str__(self):
        return f"Invoice {self.id}"

class InvoiceItem(models.Model):
    invoice = models.ForeignKey(Invoice, on_delete=models.CASCADE)
    description = models.CharField(max_length=200)
    quantity = models.IntegerField()
    price_per_unit = models.DecimalField(max_digits=8, decimal_places=2) 

    def subtotal(self):
        return self.quantity * self.price_per_unit