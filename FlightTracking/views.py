from django.shortcuts import render
from A2Core.models import Flight

# Create your views here.
def index_page(request):
    return render(request, 'main.html', {})

def search_flights_results(request):
    if request.method == 'POST':
        departure_query = request.POST.get('departure_point')
        arrival_query = request.POST.get('arrival_point')

        results = Flight.objects.filter(
            departure_point__icontains=departure_query,
            arrival_point__icontains=arrival_query
        )

        return render(request, 'result.html', {'results': results})
    
    return render(request, 'result.html', {})
