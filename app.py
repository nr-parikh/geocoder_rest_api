# Impler necessary modules
from flask import Flask, jsonify, abort, render_template
from geocoder import Geocoder

# Define the app
app = Flask(__name__)

# Define what happens when '/' is called 
@app.route('/', methods=['GET'])
def default():
	# Render the webpage
	return render_template('layout.html')

# Define what happends when '/sendRequest/<query>' is called 
@app.route('/sendRequest/<string:query>', methods=['GET'])
def get(query):

	# Create new object
	geocdr = Geocoder()

	# Check if the quesry is not empty. If empty abort and generate Bad Request error 
	if len(query) == 0:
		abort(400)

	# Call the googleGeocoder function with query
	response_json = geocdr.googleGeocoder(search=query)

	# Check the status of the response 
	if response_json['status'] == 'OK':
		# return jsonify(response_json['results'][0]['geometry']['location'])
		
		# Retrieve the coordinates
		position = response_json["results"][0]["geometry"]["location"]
		
		# Retrieve the place_id
		place_id = response_json["results"][0]["place_id"]
		
		# Check the length of the place_id. If empty, generate bad request error
		if len(place_id) == 0:
			abort(400)
		
		# Call the googlePlace function with place_id
		url = geocdr.googlePlace(place_id=str(place_id))["result"]["url"]

		# Convert the information in JSON object and send to Javascript
		return jsonify({"result" : url, "position" : position})

	else:

		# Call the hereGeocoder function with query
		response_json = geocdr.hereGeocoder(search=query)

		# Check if the response is empty
		if response_json['Response']['View']:
			# return jsonify(response_json['Response']['View'][0]['Result'][0]['Location']['DisplayPosition'])
			
			# Retrieve the position information
			position = response_json['Response']['View'][0]['Result'][0]['Location']['DisplayPosition']
			lat = position['Latitude']
			lng = position['Longitude']
			
			# Check if lat and lng are present. If not, generate bad request error 
			if not lat and lng:
				abort(400)
			
			# Call the herePlace function
			url = geocdr.herePlace(str(lat), str(lng))

			# Convert the information in JSON object and senfd to Javascript
			return jsonify({'result' : url, 'position': position})
		
		else: 

			# Return an error message 
			return "Couldn't find anything for the query {}. \n".format(query)


# Execute the following section if this file is ran 
if __name__ == '__main__':

	# Run the app
	app.run(debug=True)