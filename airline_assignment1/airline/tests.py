from django.test import TestCase, Client
from .models import Flight, Booking, Passenger
from django.contrib.auth.models import User

# Create your tests here.
class Test(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='isabella', password='password')
        self.passenger = Passenger.objects.create(
            user=self.user,
            name='Isabella',
            passport_number='1111122222',
            phone='0852600903'
        )
        self.flight = Flight.objects.create(
            flight_number='DUB097',
            departure='Dublin',
            destination='Japan',
            departure_time='2026-06-05 10:00:00',
            arrival_time='2026-06-05 20:00:00',
            price=900
        )

    # create a booking, checks if created
    def testBooking(self):
            self.client.login(username='isabella', password='password')
            Booking.objects.create(
                flight=self.flight,
                passenger=self.passenger,
                status='confirmed',
                seat_class='business'
            )
            self.assertEqual(Booking.objects.count(), 1)

    # registers a user and checks if they are redirectedto login and then checks if user is created successfully in db 
    def testRegister(self):
         response = self.client.post('/register/', {
            'username': 'testRegister',
            'password': 'password',
            'name': 'Test Register',
            'passport_number': '1234567890',
            'phone': '0852600903'
         })
         self.assertEqual(response.status_code, 302) 
         self.assertTrue(User.objects.filter(username='testRegister').exists())

    # checks is login page is accessible by user
    def testLoginPage(self):
        response = self.client.get('/login/')
        self.assertEqual(response.status_code, 200)
    
    # test register page 
    def testRegisterPage(self):
        response = self.client.get('/register/')
        self.assertEqual(response.status_code, 200)

    # test invoice page
    def testInvoicePage(self):
        self.client.login(username='isabella', password='password')
        response = self.client.get('/invoices/')
        self.assertEqual(response.status_code, 200)

   # checks if user gets redirected to login page when theyre not logged in and tries access another page
    def testLoginRedirect(self):
        self.client.login(username='isabella', password='password')
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)

    # checks if user gets redirected to login when not logged in 
    def testNotLoggedInRedirect(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 302)

    #tset string for flight details
    def testFlightDetails(self):
         self.assertEqual(str(self.flight), "flight number: DUB097, departure: Dublin, destination: Japan")

    def testPassengerDetails(self):
        self.assertEqual(str(self.passenger), "Isabella")

    

    


    


