"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_cors import CORS
from utils import APIException, generate_sitemap
from datastructures import FamilyStructure
#from models import Person

app = Flask(__name__)
app.url_map.strict_slashes = False
CORS(app)

# create the jackson family object
jackson_family = FamilyStructure("Jackson")

# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)

@app.route('/members', methods=['GET'])
@app.route('/member/<int:id>', methods=['GET'])
def get_member(id = None):

    if id == None:
        members = jackson_family.get_all_members()
        return jsonify(members), 200 
    else:
        member = jackson_family.get_member(id)
        return jsonify(member), 200 

@app.route('/member', methods=['POST'])
def add_member():

    jackson_family.first_name = request.json.get('first_name')
    jackson_family.age = request.json.get('age')
    jackson_family.lucky_numbers = request.json.get("lucky_numbers")
    jackson_family.id = request.json.get('id')

    if not jackson_family.first_name or jackson_family.first_name == "":
        return jsonify({"msg: please insert a name"}), 404 

    if not jackson_family.age or jackson_family.age == "":
        return jsonify({"msg: please insert an age"}), 404 

    if not jackson_family.lucky_numbers or jackson_family.lucky_numbers == []:
        return jsonify({"msg: please insert a lucky number"}), 404 

    member = {
        "first_name": jackson_family.first_name,
        "age": jackson_family.age,
        "lucky_numbers": jackson_family.lucky_numbers,
        "id": jackson_family.id
    }
    jackson_family.add_member(member)
    return jsonify(), 200

@app.route('/member/<int:id>', methods=['DELETE'])
def delete_member(id):

    if id == None:
        return jsonify({"msg":"Invalid ID"}), 404
    else:
        jackson_family.delete_member(id)
        resp = {"done": True}
        return jsonify(resp), 200
    

# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=True)
