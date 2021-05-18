from django.shortcuts import render
from .models import Hotel
from .forms import CityForm


def home(request):
    form = CityForm(request.POST)
    hotels = Hotel.objects.all()
    if request.method == "POST" and form.is_valid():
        city = form.cleaned_data['city']
        hotels = Hotel.objects.filter(city=city)
    return render(request, 'hotels/base.html', {'form': form, 'hotels': hotels})




