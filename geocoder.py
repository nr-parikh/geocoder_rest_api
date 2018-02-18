# Import necesarry modules
import json
import urllib.request, urllib.parse

# Class for the Geocoder API
class Geocoder():
	
	# Contructor of the class 
	def __init__(self):

		# Initialize variables 
		self.google_api_key_ = 'AIzaSyDrCduEdqjyvBoyUadOOVMWupALzpiLa7c'
		self.here_app_id_ = 'Mnswcv5a6ivjZ2XGDR4s'
		self.here_app_code_ = 'EZ1qqKVhs452aUBKdUe1Gg'

		self.google_geocode_url_ = "https://maps.googleapis.com/maps/api/geocode/json"
		self.google_places_url_ = "https://maps.googleapis.com/maps/api/place/details/json"
		self.here_geocode_url_ = "https://geocoder.cit.api.here.com/6.2/geocode.json"
		self.here_places_url_ = "https://wego.here.com/?x=ep&map="		

	# Function that takes serach string and returns the response
	def googleGeocoder(self, search=""):

		# Create a dictionary to store the parameters used for constructing the request
		values = dict()
		values['address'] = search
		values['key'] = self.google_api_key_

		# Parse the parameters
		payload = urllib.parse.urlencode(values)

		# Create complete URL 
		complete_url = self.google_geocode_url_ + '?' + payload

		# Get the response 
		response = urllib.request.urlopen(complete_url)
		
		# Read the data 
		data = response.read()

		# Define the encoding 
		encoding = response.info().get_content_charset('utf-8')

		# Decode the JSON data
		response_json = json.loads(data.decode(encoding))

		return response_json	

	# Function that takes in the unique place_id and returns the response
	def googlePlace(self, place_id=""):
		
		# Create a dictionary to store the parameters used for constructing the request
		values = dict()
		values['key'] = self.google_api_key_
		values['place_id'] = place_id

		# Parse the parameters
		payload = urllib.parse.urlencode(values)

		# Create complete URL 
		complete_url = self.google_places_url_ + '?' + payload

		# Get the response 
		response = urllib.request.urlopen(complete_url)
		
		# Read the data 
		data = response.read()

		# Define the encoding 
		encoding = response.info().get_content_charset('utf-8')

		# Decode the JSON data
		response_json = json.loads(data.decode(encoding))

		return response_json		

	# Function that takes serach string and returns the response
	def hereGeocoder(self, search=""):

		# Create a dictionary to store the parameters used for constructing the request
		values = dict()
		values['app_id'] = self.here_app_id_
		values['app_code'] = self.here_app_code_
		values['searchtext'] = search

		# Parse the parameters
		payload = urllib.parse.urlencode(values)

		# Create complete URL 
		complete_url = self.here_geocode_url_ + '?' + payload

		# Get the response 
		response = urllib.request.urlopen(complete_url)

		# Read the data 
		data = response.read()

		# Define the encoding 
		encoding = response.info().get_content_charset('utf-8')

		# Decode the JSON data		
		response_json = json.loads(data.decode(encoding))

		return response_json		

	def herePlace(self, lat="", lng=""):

		# Create the complete URL by combining lat and lng values
		complete_url = self.here_places_url_ + lat + ',' + lng + ',' + '14'

		return complete_url

# Execute the following section if this file is ran 
if __name__ == "__main__":

	# Create the object
	geocdr = Geocoder()

	# Define query
	query = "San Francisco"
	# Call the googleGeocder function
	# NOTE: To get position from JSON object follow convention "<response>['results'][0]['geometry']['location']" 
	# while using Google Maps	
	response_json = geocdr.googleGeocoder(str(query))
	position = response_json['results'][0]['geometry']['location']
	
	# Retrieve the unique place_id
	place_id = response_json["results"][0]["place_id"]
	
	# Pass the place_id to googlePlace function
	url = geocdr.googlePlace(str(place_id))["result"]["url"]

	print("\n{} is located at: ".format(query))
	print(position)
	print("Visit the URL below to open maps:")
	print(url)
	print("Found using Google geocoder API.\n")

	# Call the hereGeocoder function
	# NOTE: To get position from JSON object follow convention "<response>['Response']['View'][0]['Result'][0]['Location']['DisplayPosition']"
	# while using Here geocoder
	response_json = geocdr.hereGeocoder(str(query))
	position = response_json['Response']['View'][0]['Result'][0]['Location']['DisplayPosition']
	
	# Get the latitude and longitude values
	lat = position['Latitude']
	lng = position['Longitude']

	# Pass the coordinates to herePlace function
	url = geocdr.herePlace(lat=str(lat), lng=str(lng))

	print(position)
	print("Visit the URL below to open maps:")
	print(url)
	print("Found using Here geocoder API.")	