from flask import request, Flask, jsonify
from helper import *

app = Flask(__name__) 

@app.route('/store', methods=['POST'])
def store():
	response = store_email()
	return jsonify({
		'message' : 'Inbox messages stored in database'
	})

@app.route('/filter1', methods=['POST'])
def filter1():
	data = request.get_json()
	email_id = data['email_id']
	response = filter_emailid(email_id)
	return jsonify(response)


if __name__ == '__main__':
    app.run(debug=True)
