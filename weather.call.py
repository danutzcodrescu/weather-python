import httplib2
import json
import datetime
import os
from dotenv import load_dotenv
load_dotenv()

def weather(address):
  url = f"https://maps.googleapis.com/maps/api/geocode/json?key={os.environ['GMAPS_API_KEY']}&address={address}"

  _, content = httplib2.Http().request(url)

  json_data = json.loads(content)
  location = json_data['results'][0]['geometry']['location']

  url = f"https://api.darksky.net/forecast/{os.environ['DARK_SKY_API_KEY']}/{str(location['lat'])},{str(location['lng'])}?units=si&exclude=flags,alerts"

  _, content = httplib2.Http().request(url)

  json_data = json.loads(content)

  time = datetime.datetime.fromtimestamp(
      json_data['currently']['time']).strftime('%Y-%m-%d %H:%M:%S')

  currently = {'Time': time, 'Temperature': json_data['currently']
              ['temperature'], 'Wind': json_data['currently']['windSpeed'], 'PrecipitationProbability': json_data['currently']['precipProbability']}

  hourDict = {'Summary': json_data['hourly']['summary']}
  for hour in json_data['hourly']['data']:
      time = datetime.datetime.fromtimestamp(
          hour['time']).strftime('%Y-%m-%d %H:%M')
      hourData = {'Time': time, 'Temperature': hour
                ['temperature'], 'Wind': hour['windSpeed'], 'PrecipitationProbability': hour['precipProbability']}
      hourDict[time] = hourData
  return json.JSONEncoder().encode({'currently': currently, 'hourly': hourDict})

address = input('Provide the location: ')

print(weather(address.replace(' ', '%20')))


