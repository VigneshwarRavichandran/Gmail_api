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
	response = None
	if predicate == 'ALL':
		response = filter_all(email_id, contains)
	elif predicate == 'ANY':
		response = filter_any(email_id, contains)
	return jsonify(response)


if __name__ == '__main__':
    app.run(debug=True)
