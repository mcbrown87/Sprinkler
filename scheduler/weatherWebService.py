import json
import urllib2

class WeatherWebService:
	def __init__(self):
		self._endpoint = "http://api.openweathermap.org/data/2.5/weather?lat=43.792687&lon=-70.430532&appid=1963a6b41a6c18337d5160732408f58a"

	def CurrentWeather(self):
		return json.load(urllib2.urlopen(self._endpoint))['weather'][0]['main']