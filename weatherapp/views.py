import requests
from django.shortcuts import render, redirect
from .models import City
from .forms import CityForm


def home(request):
    url = 'http://api.openweathermap.org/data/2.5/find?q={}&units=metric&appid=a07df7855b3a2fd4b88182c3982f9459'
    error_msg = ""
    message = ''
    message_class = ''
    if request.method == 'POST':
        form = CityForm(request.POST)

        if form.is_valid():
            new_city = form.cleaned_data['name']
            existing_city_count = City.objects.filter(
                name__iexact=new_city).count()
            print(existing_city_count)
            if existing_city_count == 0:
                ro = requests.get(url.format(new_city)).json()
                print(ro)
                if ro['count'] != 0:
                    form.save()
                else:
                    error_msg = "Invalid city"

            else:
                error_msg = "City already exists!"

        if error_msg:
            message = error_msg
            message_class = 'is-danger'
        else:
            message = 'City added successfully!'
            message_class = 'is-success'

    form = CityForm()

    cities = City.objects.all()

    weather_data = []

    for city in cities:
        r = requests.get(url.format(city)).json()
        print(r)
        city_weather = {
            'city': city.name,
            'temperature': r['list'][0]['main']['temp'],
            'feels_like': r['list'][0]['main']['feels_like'],
            'temp_min': r['list'][0]['main']['temp_min'],
            'temp_max': r['list'][0]['main']['temp_max'],
            'description': r['list'][0]['weather'][0]['description'],
            'icon': r['list'][0]['weather'][0]['icon']
        }

        weather_data.append(city_weather)

    context = {
        'weather_data': weather_data,
        'form': form,
        'message': message,
        'message_class': message_class
    }

    return render(request, 'home.html', context)


def dcity(request, city_name):
    City.objects.get(name=city_name).delete()
    return redirect('home')
