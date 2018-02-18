import json
import urllib.request, urllib.parse

class Geocoder():
	def __init__(self):

		self.google_api_key_ = 'AIzaSyDrCduEdqjyvBoyUadOOVMWupALzpiLa7c'
		self.here_app_id_ = 'Mnswcv5a6ivjZ2XGDR4s'
		self.here_app_code_ = 'EZ1qqKVhs452aUBKdUe1Gg'

		self.google_geocode_url_ = 'https://maps.googleapis.com/maps/api/geocode/json'
		self.here_geocode_url_ = 'https://geocoder.cit.api.here.com/6.2/geocode.json'

	def googleGeocoder(self, search=""):

		values = dict()
		values['address'] = search
		values['key'] = self.google_api_key_

		payload = urllib.parse.urlencode(values)

		complete_url = self.google_geocode_url_ + '?' + payload

		response = urllib.request.urlopen(complete_url)
		data = response.read()

		encoding = response.info().get_content_charset('utf-8')

		response_json = json.loads(data.decode(encoding))

		return response_json	

	def hereGeocoder(self, search=""):

		values = dict()
		values['app_id'] = self.here_app_id_
		values['app_code'] = self.here_app_code_
		values['searchtext'] = search

		payload = urllib.parse.urlencode(values)

		complete_url = self.here_geocode_url_ + '?' + payload

		response = urllib.request.urlopen(complete_url)
		data = response.read()

		encoding = response.info().get_content_charset('utf-8')

		response_json = json.loads(data.decode(encoding))

		return response_json		


if __name__ == "__main__":

	geocdr = Geocoder()

	print("Enter the place to be searched:")
	query = input()
	response_json = geocdr.googleGeocoder(str(query))
	position = response_json['results'][0]['geometry']['location']

	print("\n{} is located at: ".format(query))
	print(position)

	response_json = geocdr.hereGeocoder(str(query))
	position = response_json['Response']['View'][0]['Result'][0]['Location']['DisplayPosition']

	print(position)