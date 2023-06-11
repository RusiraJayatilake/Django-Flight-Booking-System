from django.urls import path
from . import views

urlpatterns = [
    path('', views.main_page, name='main_page'),
    path('flights/', views.flight_list, name='flight_list'),
    path('flightsform/', views.add_flights, name='add_flights'),
    path('customerdata/', views.customer_list, name='customer_list'),
    path('customer/', views.customer_form, name='customer_form'),
    path('booking/', views.add_bookings, name='add_bookings'),
    path('search/', views.search_flights, name='search_flights'),
    path('searchbooking/', views.search_bookings, name='search_bookings'),
    path('cancel/', views.cancel_booking, name='cancel_booking'),
]