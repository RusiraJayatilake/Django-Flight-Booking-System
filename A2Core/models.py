from django.db import models
from django.utils.crypto import get_random_string

# Create your models here.
class Flight(models.Model):
    flight_id = models.CharField(max_length=4, primary_key=True, unique=True)
    flight_name = models.CharField(max_length=100)
    departure_point = models.CharField(max_length=4)
    arrival_point = models.CharField(max_length=4)
    departure_datetime = models.DateTimeField()
    arrival_datetime = models.DateTimeField()
    price = models.PositiveIntegerField()
    seats_booked = models.PositiveIntegerField()
    max_seats = models.PositiveIntegerField()

    def __str__(self):
        return f"{self.flight_name} ({self.flight_id})"
    
    def save(self, *args, **kwargs):
        if not self.flight_id:
            # Generate a unique 4-character ID
            self.flight_id = get_random_string(length=4)

        super().save(*args, **kwargs)


class Customer(models.Model):
    customer_id = models.CharField(max_length=4, primary_key=True, unique=True)
    customer_name = models.CharField(max_length=100)
    customer_email = models.EmailField()

    def __str__(self):
        return 'Name: ' + self.customer_name + ', Email: ' + self.customer_email + '<br>'

    def save(self, *args, **kwargs):
        if not self.customer_id:
            # Generate a unique 4-character ID
            self.customer_id = get_random_string(length=4)

        super().save(*args, **kwargs)


class Booking(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    flight = models.ManyToManyField(Flight)
    booking_reference = models.CharField(max_length=10, unique=True, primary_key=True)

    def __str__(self):
        return self.booking_reference
    
    def save(self, *args, **kwargs):
        if not self.booking_reference:
            # Generate a unique booking reference 
            customer_id = self.customer.customer_id
            flight_ids = "".join([flight.flight_id for flight in self.flight.all()])
            booking_reference = f"{customer_id}{flight_ids}{get_random_string(length=2)}"
            self.booking_reference = booking_reference

        super().save(*args, **kwargs)
