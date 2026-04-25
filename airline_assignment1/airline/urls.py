from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('flight/<int:flight_id>/', views.flight_detail, name='flight_detail'),
    path('book/<int:flight_id>/', views.book_a_flight, name='book_a_flight'),
    path('bookings/', views.bookings, name='bookings'),
    path('invoices/', views.invoices, name='invoices'),

]