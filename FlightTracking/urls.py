from django.urls import path
from . import views

app_name = 'Flight Tracking System'
urlpatterns = [
    path('main/', views.index_page, name='main_page'),
    path('searchresults/', views.search_flights_results, name='search_flights_results'), 
]