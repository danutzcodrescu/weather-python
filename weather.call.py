import httplib2
import json
import datetime
import os
from dotenv import load_dotenv
load_dotenv()

def getLocation(address):
  url = f"https://maps.googleapis.com/maps/api/geocode/json?key={os.environ['GMAPS_API_KEY']}&address={address}"
  try:
    _, content = httplib2.Http().request(url)

    json_data = json.loads(content)
    return json_data['results'][0]['geometry']['location']
  except httplib2.ServerNotFoundError:
    print('error in gmaps')

def getWeatherData(location): 
  url = f"https://api.darksky.net/forecast/{os.environ['DARK_SKY_API_KEY']}/{str(location['lat'])},{str(location['lng'])}?units=si&exclude=flags,alerts"
  try:
    _, content = httplib2.Http().request(url)

    return json.loads(content)
  except httplib2.ServerNotFoundError:
    print('error in darksky')

def weather(address):
  
  location = getLocation(address)
  weatherData = getWeatherData(location)

  time = datetime.datetime.fromtimestamp(
      weatherData['currently']['time']).strftime('%Y-%m-%d %H:%M:%S')

  currently = {'Time': time, 'Temperature': weatherData['currently']
              ['temperature'], 'Wind': weatherData['currently']['windSpeed'], 'PrecipitationProbability': weatherData['currently']['precipProbability']}

  hourDict = {'Summary': weatherData['hourly']['summary']}
  for hour in weatherData['hourly']['data']:
      time = datetime.datetime.fromtimestamp(
          hour['time']).strftime('%Y-%m-%d %H:%M')
      hourData = {'Time': time, 'Temperature': hour
                ['temperature'], 'Wind': hour['windSpeed'], 'PrecipitationProbability': hour['precipProbability']}
      hourDict[time] = hourData
  return json.JSONEncoder().encode({'currently': currently, 'hourly': hourDict})

address = input('Provide the location: ')

print(weather(address.replace(' ', '%20')))


