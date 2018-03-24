from flask import *
from database import mongo, current_user

investor_api = Blueprint('investor_api', __name__)

from bson import ObjectId
import json

class JSONEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, ObjectId):
            return str(o)
        return json.JSONEncoder.default(self, o)

investments = mongo['db']['investments']
farmers = mongo['db']['testFarm']

@investor_api.route('/investor', methods=['GET','SET'])
def investor():
    if request.method == 'GET':
        return render_template('investor.html')

@investor_api.route('/get_investments')
def get_investments():
	if request.method == 'GET':
		l = []
		for i in investments.find({'investor_id': request.args.get('investor_id')}):
			i.pop('_id',None)
			l.append(i)
		return jsonify(l)

@investor_api.route('/get_available_investments')
def get_available_investments():
	if request.method == 'GET':
		l = []
		for f in farmers.find():
			l.append(f)
		return jsonify(l)

@investor_api.route('/invest',methods=['GET'])
def invest():
		farmer_id = request.args.get('farmer_id')
		investor_id = request.args.get('investor_id', default = current_user)
		amount = request.args.get('amount')
		investments.insert({
			'farmer_id':farmer_id,
			'investor_id': investor_id,
			'amount': amount
			})
		return jsonify({'status': 200})



