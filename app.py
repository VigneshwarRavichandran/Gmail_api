from flask import request, Flask, jsonify
from helper import *

app = Flask(__name__) 

@app.route('/store', methods=['POST'])
def store():
	response = store_email()
	return jsonify({
		'message' : response
	})

@app.route('/filter', methods=['POST'])
def filter():
	try:
		data = request.get_json()
		predicate = data['predicate']
		email_id = data['filter']['from']
		contains = data['filter']['contains']
		days = data['filter']['less_than']
		action = data['action']
	except:
		return jsonify({
			"message" : "Provide all the necessary fields!"
		})
	response = None
	if predicate == 'ALL':
		response = filter_all(email_id, contains, days, action)
	elif predicate == 'ANY':
		response = filter_any(email_id, contains, days, action)
	return jsonify({
		"message" : response
	})


if __name__ == '__main__':
    app.run(debug=True)
