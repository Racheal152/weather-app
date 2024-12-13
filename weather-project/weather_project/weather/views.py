from django.shortcuts import render
import requests
import datetime

def index(request):
    api_key = '5b322908a8d651aff96df40a697d2791' 
    current_weather_url = 'https://api.openweathermap.org/data/2.5/weather?q={}&appid={}'
    forecast_url = 'https://api.openweathermap.org/data/2.5/onecall?lat={}&lon={}&exclude=current,minutely,hourly,alerts&appid={}'
    
    context = {}
    
    if request.method == 'POST':
        city = request.POST.get('city')
        print(f"City entered: {city}")
        
        weather_data, daily_forecasts = fetch_weather_and_forecast(city, api_key, current_weather_url, forecast_url)

        if weather_data:
            context['weather_data'] = weather_data
        else:
            context['error'] = "Unable to fetch weather data. Please check the city name or try again later."
        
        if daily_forecasts:
            context['daily_forecasts'] = daily_forecasts

    return render(request, 'weather/index.html', context)

def fetch_weather_and_forecast(city, api_key, current_weather_url, forecast_url):
    try:
        weather_response = requests.get(current_weather_url.format(city, api_key)).json()
        print("Weather API response:", weather_response)

        if weather_response.get('cod') != 200:
            print(f"Error fetching weather data: {weather_response}")
            return None, None

        weather_data = {
            'name': weather_response['name'],
            'temperature': round(weather_response['main']['temp'] - 273.15, 2),
            'description': weather_response['weather'][0]['description'],
            'icon': weather_response['weather'][0]['icon'],
        }

    
        forecast_url = 'https://api.openweathermap.org/data/2.5/forecast?q={}&appid={}'
        forecast_response = requests.get(forecast_url.format(city, api_key)).json()
        print("Forecast API response:", forecast_response)

        if forecast_response.get('cod') != "200":
            print(f"Error fetching forecast data: {forecast_response}")
            return weather_data, None

        daily_forecasts = []
        for forecast in forecast_response['list'][::8]:  
            daily_forecasts.append({
                'day': datetime.datetime.fromtimestamp(forecast['dt']).strftime('%A'),
                'min_temp': round(forecast['main']['temp_min'] - 273.15, 2),
                'max_temp': round(forecast['main']['temp_max'] - 273.15, 2),
                'description': forecast['weather'][0]['description'],
                'icon': forecast['weather'][0]['icon'],
            })

        return weather_data, daily_forecasts

    except Exception as e:
        print(f"An error occurred: {e}")
        return None, None
