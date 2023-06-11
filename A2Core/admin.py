from django.contrib import admin
from .models import Flight, Customer, Booking

# Register your models here.
admin.site.register(Flight)
admin.site.register(Customer)
admin.site.register(Booking)
