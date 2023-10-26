from flask import Flask, request, jsonify
import requests
from datetime import datetime
import xml.etree.ElementTree as ET

app = Flask(__name__)

@app.route('/')
def hello_world():
  return 'Hi!'

@app.route('/get_tomorrow_temperature', methods=['GET'])
def get_tomorrow_temperature():
    latitude = request.args.get('latitude')
    longitude = request.args.get('longitude')

    # Perform the internal request to Open Meteo API using latitude and longitude
    open_meteo_url = f'https://api.open-meteo.com/v1/forecast?latitude={latitude}&longitude={longitude}&forecast_days=2&hourly=temperature_2m&timezone=PST'
    response = requests.get(open_meteo_url)

    if response.status_code == 200:
        data = response.json()
        temperatures = data['hourly']['temperature_2m']
        timestamp = data['hourly']['time']

        # Extract temperatures based on the selected time range
        temperature_data = []
        for i, hour in enumerate(timestamp):
            if (i >= 24):
              hour = int(hour.split('T')[1].split(':')[0])
              temperature_data.append({'time': hour, 'temperature_2m': temperatures[i]})
        return jsonify(temperature_data)
    else:
        return jsonify({'error': 'Failed to fetch data from Open Meteo API'}), response.status_code

@app.route('/get_next_7d_temperature', methods=['GET'])
def get_next_7d_temperature():
    latitude = request.args.get('latitude')
    longitude = request.args.get('longitude')

    # Perform the internal request to Open Meteo API using latitude and longitude
    open_meteo_url = f'https://api.open-meteo.com/v1/forecast?latitude={latitude}&longitude={longitude}&forecast_days=8&hourly=temperature_2m&timezone=PST'
    response = requests.get(open_meteo_url)

    if response.status_code == 200:
        data = response.json()
        temperatures = data['hourly']['temperature_2m']
        timestamp = data['hourly']['time']

        # Extract temperatures based on the selected time range
        temperature_data = []
        for i, hour in enumerate(timestamp):
            if (24 <= i < 24*8):
                time = hour.split('T')[1].split(':')[0]
                date = hour.split('T')[0]
                temperature_data.append({'date': date, 'time': time, 'temperature_2m': temperatures[i]})

        return jsonify(temperature_data)
    else:
        return jsonify({'error': 'Failed to fetch data from Open Meteo API'}), response.status_code


# Ruta para buscar la ubicación de una ciudad en la API de Nominatim
@app.route('/search_city')
def search_city():
  print("ga")
  # Obtén el valor del parámetro 'city' de la URL
  city = request.args.get('city')

  # Verifica si se proporcionó el parámetro 'city'
  if not city:
    return jsonify({'error': 'El parámetro "city" es obligatorio'}), 400

  # URL de la API de Nominatim
  api_url = 'https://nominatim.openstreetmap.org/search'

  # Parámetros de la solicitud
  params = {
    'q': city,
    'format': 'json'
  }

  # Realiza la solicitud a la API de Nominatim
  response = requests.get(api_url, params=params)
  # Verifica si la solicitud fue exitosa
  if response.status_code == 200:
    data = response.json()
    result = {
    "lat": data[0]['lat'],
    "lon": data[0]['lon']
    }   

    return jsonify(result)
  else:
    return jsonify({'error': 'Error al realizar la solicitud a la API'}), 500

if __name__ == '__main__':
  app.run(debug=True)