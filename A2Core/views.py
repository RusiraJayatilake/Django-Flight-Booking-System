from django.shortcuts import redirect, render
from django.http import HttpResponse
from .models import Flight, Customer, Booking
from datetime import datetime
import string
import random

# Create your views here.
def main_page(request):    
    return render(request, 'index.html', {})
    

def customer_form(request):
    if request.method == 'POST':
        customer_name = request.POST['customer_name']
        customer_email = request.POST['customer_email']

        new_customer = Customer.objects.create(
            customer_name=customer_name,
            customer_email=customer_email
        )

        return render(request, "make_booking.html", {'customer': new_customer})

    return render(request, "make_booking.html", {})


def customer_list(request):
    customers = Customer.objects.all()
    return HttpResponse(customers)

# add flights
def add_flights(request):
    if request.method == 'POST':
        flight_name = request.POST['flight_name']
        departure_point = request.POST['departure_point']
        arrival_point = request.POST['arrival_point']
        departure_datetime = request.POST['departure_datetime']
        arrival_datetime = request.POST['arrival_datetime']
        price = request.POST['price']
        seats_booked = request.POST['seats_booked']
        max_seats = request.POST['max_seats']

        new_flight = Flight(
            flight_name=flight_name,
            departure_point=departure_point,
            arrival_point=arrival_point,
            departure_datetime=departure_datetime,
            arrival_datetime=arrival_datetime,
            price=price,
            seats_booked=seats_booked,
            max_seats=max_seats,
        )

        new_flight.save()

    return render(request, "add_flights.html", {})

# show to flights list 
def flight_list(request):
    flights = Flight.objects.all()
    return render(request, 'index.html', {'flights': flights})


# generate a random string for the booking reference 
def generate_random_string(lenght=2):
    chars = string.ascii_letters + string.digits
    return ''.join(random.choice(chars) for _ in range(lenght))

# add bookings
def add_bookings(request):
    if request.method == 'POST':
        # Process booking form submission
        customer_id = request.POST.get('customer_id', '')
        flight_id = request.POST.get('flight_id', '')

        try:
            customer = Customer.objects.get(pk=customer_id)
            flight = Flight.objects.get(pk=flight_id)

            if flight.seats_booked >= flight.max_seats:
                return render(request, 'make_booking.html', {'error': 'This flight is already full.'})

            # Generate unique booking reference 
            booking_reference = f"{customer_id}-{flight_id}-{generate_random_string()}"

            # Create the booking
            booking = Booking.objects.create(
                booking_reference=booking_reference,
                customer=customer,
            )

            booking.flight.add(flight)

            # Retrieve the updated flight object with the related bookings
            flight = Flight.objects.get(pk=flight_id)

            return render(request, 'make_booking.html', {'booking_reference': booking_reference, 'customer': customer, 'flight': flight})

        except Customer.DoesNotExist:
            return render(request, "make_booking.html", {'error': 'Invalid customer ID'})

        except Flight.DoesNotExist:
            return render(request, "make_booking.html", {'error': 'Invalid flight ID'})

    return render(request, "make_booking.html", {})


# Search flights
def search_flights(request):
    if request.method == 'POST':
        dp_date = request.POST.get('departure_date')
        ar_date = request.POST.get('arrival_date')

        if dp_date and ar_date:
            try:
                # Convert the date strings to datetime objects
                dp_date = datetime.strptime(dp_date, '%Y-%m-%d').date()
                ar_date = datetime.strptime(ar_date, '%Y-%m-%d').date()
            except ValueError:
                # Handle invalid date format
                return render(request, 'index.html', {'error': 'Invalid date format'})

            # Query flights based on departure and arrival dates
            flights = Flight.objects.filter(departure_datetime__range=[dp_date, ar_date])
        else:
            # No search parameters provided, return all flights
            flights = Flight.objects.all()

        return render(request, 'index.html', {'flights': flights})
    else:
        return render(request, 'index.html', {})


# search for bookings
def search_bookings(request):
    if request.method == 'POST':
        booking_reference = request.POST.get('booking_reference')

        try:
            booking = Booking.objects.get(booking_reference=booking_reference)
            customer = booking.customer
            flights = booking.flight.all()

            return render(request, 'search_booking.html', {'booking_reference': booking_reference, 'customer': customer, 'flights': flights})
        except Booking.DoesNotExist:
            error_message = 'Invalid booking reference. Please try again.'
            return render(request, 'search_booking.html', {'error': error_message})

    return render(request, 'search_booking.html', {})


# cancel booking
def cancel_booking(request):
    if request.method == 'POST':
        booking_reference = request.POST.get('booking_reference')

        try:
            booking = Booking.objects.get(booking_reference=booking_reference)
            booking.delete()
            return render(request, 'booking_cancelled.html', {})

        except Booking.DoesNotExist:
            error_message = 'Invalid booking reference. Please try again.'
            return render(request, 'search_booking.html', {'error': error_message})

    return render(request, 'search_booking.html', {})