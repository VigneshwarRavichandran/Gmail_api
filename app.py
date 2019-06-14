from flask import request, Flask, jsonify
from helper import *

app = Flask(__name__) 

@app.route('/store', methods=['POST'])
def store():
	response = store_email()
	return jsonify({
		'message' : 'Inbox messages stored in database'
	})

@app.route('/filter', methods=['POST'])
def filter():
	data = request.get_json()
	predicate = data['predicate']
	email_id = data['filter']['from']
	contains = data['filter']['contains']
	days = data['filter']['less_than']
	action = data['action']
	response = None
	if predicate == 'ALL':
		filter_all(email_id, contains, days)
	elif predicate == 'ANY':
		filter_any(email_id, contains, days)
	return jsonify({
		"message" : "Action performed successfully"
	})



if __name__ == '__main__':
    app.run(debug=True)
