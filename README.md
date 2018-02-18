# Geocoder RESTful API

[![Build Status](https://travis-ci.org/nr-parikh/geocoder_rest_api.svg?branch=master)](https://travis-ci.org/nr-parikh/geocoder_rest_api)
[![License](https://img.shields.io/badge/License-BSD%203--Clause-green.svg)](https://github.com/nr-parikh/geocoder_rest_api/blob/master/LICENSE)

This is a simple Geocoder RESTful API that takes in address or city name and finds out the latitude and longitude values of that place. It uses Google Maps API to first to get the values on the backend. If for some reason Google Maps API fails then as a fallback option uses Here Geocoder API. The API only has a GET method implemented in Python that runs on the backend. Frontend is written in HTML with Javascript running on the backend and communicating with the RESTful API. It uses Flask framework in Python.

## Dependencies
* Python 3.5.2
* Flask 

## Workflow 

The API is a wrapper over the Google and Here's geocoding APIs. The default server runs the frontend web page. Once the input has been provided and the *Search* button is clicked, the frontend listens to this event and passes on the information to the *javascript* running on the backend. The script creates the URL which triggers the GET method of Flask framework. The framework then queries the Google Maps and gets the response from it. It checks the status of the response if it is found to be correct then further processes the response to get the URL of the map and returs *JSON* object to the script. In case the Google Maps' response is not correct then it goes to Here API. In this case also, it checks if the response is valid or not and if it is valid then processes it otherwise returns a string stating the place couldn't be found. 

## Instructions to run the service 

Before running the code please ensure that dependencies are being met. There are two ways to run the code:
* Using the terminal 
* Using the browser 

### Using the terminal 

To run the code using the terminal please follow the instructions given below:
1. Clone the repository
2. Open the terminal 
3. Run the Flask app using `python3 <path to repository>/app.py`.
4. Open another terminal. Run the command `curl -i http://localhost:5000/sendRequest/California` if one wants to get position of *California*. If one wants to find the exact address for e.g. 3424 Tulane Drive, MD; run the command `curl -i http://localhost:5000/sendRequest/3424+Tulane+Drive+MD`.

The output on the terminal should look like below.
```
HTTP/1.0 200 OK
Content-Type: application/json
Content-Length: 199
Server: Werkzeug/0.14.1 Python/3.5.2
Date: Sun, 18 Feb 2018 05:35:38 GMT

{
  "position": {
    "lat": 38.9846817, 
    "lng": -76.9572439
  }, 
  "result": "https://maps.google.com/?q=3424+Tulane+Dr,+Hyattsville,+MD+20783,+USA&ftid=0x89b7c68c032dbca9:0x1603f42ea05e114"
}
```

### Using the browser

The first 3 steps are same as above. Follow the instructions below to check the page in browser:
1. Open the browser and type either `http://127.0.0.1:5000` or `http://localhost:5000`.
2. Type the query to be searched. Hit the search button.
3. If one wants to see the place on the map, click on the hyperlink named "Go to map!".

## Instructions to use the API

One can use the API individually to find obtain the coordinates of the place. Since the API has a class and all the functions are its methods, in order to use functions one needs to create an object of the class *Geocoder*. One needs to import the Geocoder class in the file where functionality is needed. For example, if one wants to find the coordinates of "San Francisco" using Google Maps in a function *foo*, one can write following function:
```
from geocoder import Geocoder

def foo():

	# Create new object of the class Geocoder99
	object = Geocoder()
	# Define query
	query = "San Francisco"
	# Call the googleGeocder function
	# NOTE: To get position from JSON object follow convention "<response>['results'][0]['geometry']['location']" while using Google Maps
	position_google = object.googleGeocoder(str(query))['results'][0]['geometry']['location']
	# Call the hereGeocoder function
	# NOTE: To get position from JSON object follow convention "<response>['Response']['View'][0]['Result'][0]['Location']['DisplayPosition']" while using Here geocoder
	position_here = object.hereGeocoder['Response']['View'][0]['Result'][0]['Location']['DisplayPosition']

```

If one wants to obtain the URL for the place that can be used to view on maps, few lines of code needs to be added. While using the Google API, apart from retrieving position one also needs to retrieve *place_id* that is unique for that place. On the other hand, while using Here API latitude and longitude values only will suffice. The comple code will look like below:
```
from geocoder import Geocoder

def foo():

	object = Geocoder()
	query = "San Francisco"
	
	# Store the response and retrieve whatever information is needed
	response = object.googleGeocoder(str(query))
	position_google = response['results'][0]['geometry']['location']
	place_id = response["results"][0]["place_id"] # Retreiving place_id

	# Pass the place_id to googlePlace function
	url = object.googlePlace(str(place_id))["result"]["url"]	

	position_here = object.hereGeocoder['Response']['View'][0]['Result'][0]['Location']['DisplayPosition']
	
	# Get the latitude and longitude values 
	lat, lng = position_here['Latitude'], position_here['Longitude']

	# Pass the coordinates to herePlace function
	url = object.herePlace(str(lat), str(lng))

```

