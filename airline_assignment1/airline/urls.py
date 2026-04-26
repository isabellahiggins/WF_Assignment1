from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('flight/<int:flight_id>/', views.flight_detail, name='flight_detail'),
    path('book/<int:flight_id>/', views.book_a_flight, name='book_a_flight'),
    path('bookings/', views.bookings, name='bookings'),
    path('invoices/', views.invoices, name='invoices'),
    path('login/', views.loginUser, name='login'),
    path('register/', views.registerUser, name='register'),
    path('logout/', views.logoutUser, name='logout'),
    path('passengers/', views.passengers, name='passengers'),
    path('booking/<int:booking_id>/cancel/', views.cancelBooking, name='cancel_booking'),

]