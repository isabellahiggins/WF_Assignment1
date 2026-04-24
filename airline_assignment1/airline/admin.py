from django.contrib import admin
from .models import Flight, Passenger, Booking, Invoice, InvoiceItem

# Register your models here.
admin.site.register(Flight)
admin.site.register(Passenger)
admin.site.register(Booking)
admin.site.register(Invoice)
admin.site.register(InvoiceItem)

