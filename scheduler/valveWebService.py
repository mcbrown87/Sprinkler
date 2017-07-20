import json
import urllib2
import datetime

import dateutil
import pytimeparse as pytimeparse


class ValveWebService:
	def __init__(self):
		self._endpoint = "http://192.168.1.253"

	def IsOpen(self):
		return json.load(urllib2.urlopen(self._endpoint + "/isOpen")).isOpen

	def Open(self):
		urllib2.urlopen(self._endpoint + "/openValve", "")

	def Close(self):
		urllib2.urlopen(self._endpoint + "/closeValve", "")

	def OpenDuration(self):
		return datetime.timedelta(seconds = pytimeparse.parse(json.load(urllib2.urlopen(self._endpoint + "/openDuration"))["valveOpenDuration"]))