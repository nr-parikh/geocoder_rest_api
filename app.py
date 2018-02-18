from flask import Flask, jsonify, abort, render_template
from geocoder import Geocoder

app = Flask(__name__)

@app.route('/', methods=['GET'])
def default():
	return render_template('layout.html')

@app.route('/sendRequest/<string:query>', methods=['GET'])
def get(query):

	geocdr = Geocoder()

	if len(query) == 0:
		abort(400)

	response_json = geocdr.googleGeocoder(search=query)

	if response_json['status'] == 'OK':
		# return jsonify(response_json['results'][0]['geometry']['location'])
		position = response_json["results"][0]["geometry"]["location"]
		place_id = response_json["results"][0]["place_id"]
		
		if len(place_id) == 0:
			abort(400)
		
		url = geocdr.googlePlace(place_id=str(place_id))["result"]["url"]
		return jsonify({"result" : url, "position" : position})

	else:
		response_json = geocdr.hereGeocoder(search=query)

		if response_json['Response']['View']:
			# return jsonify(response_json['Response']['View'][0]['Result'][0]['Location']['DisplayPosition'])
			position = response_json['Response']['View'][0]['Result'][0]['Location']['DisplayPosition']
			lat = position['Latitude']
			lng = position['Longitude']
			
			if not lat and lng:
				abort(400)
			
			url = geocdr.herePlace(str(lat), str(lng))
			return jsonify({'result' : url, 'position': position})
		else: 
			return "Couldn't find anything for the query {}. \n".format(query)


if __name__ == '__main__':
	app.run(debug=True)