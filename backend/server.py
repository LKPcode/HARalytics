
import random
from flask import Flask, url_for, jsonify
from auth import *
from werkzeug.utils import secure_filename
import os
import json

from database import MySQL

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = "./uploads"
db = MySQL()

# url_for('static', filename='style.css')


@app.route('/signin', methods=['POST'])
def signin():
    user = request.json
    user["ip"] = "8.8.8.8"  # request.remote_addr
    user["isp"] = "Wind"
    if not db.user_exists(user):
        db.create_user(user)
        return jsonify({"token": encode_jwt(user).decode("utf-8")}), 201
    else:
        return jsonify({"msg": "user already exists"}), 401


@app.route('/login', methods=['POST'])
def login():
    user = request.json
    print(user)
    # if user validates in database
    if db.user_exists(user):
        return jsonify({"token": encode_jwt(user).decode("utf-8")}), 201
    else:
        return jsonify({"msg": "user credentials are not correct"}), 401


@app.route("/upload", methods=["POST"])
@authentication_required
def upload_data():
    data = request.json
    print(request.user, "HELLLOOO")
    try:
        db.insert_data(data, request.user)
        return jsonify({"msg": "upload was succesfull"}), 200
    except Exception as e:
        print(f"Error: {e}")
        return jsonify({"msg": e}), 500


@app.route("/heatmap", methods=["GET"])
@authentication_required
def send_heatmap_data():

    data = db.get_heatmap_data_of_user(request.user["email"])

    new_structure = []
    for row in data:
        new_structure.append([row["x"], row["y"], 1.0])

    json_string = json.dumps(new_structure)
    print(json_string)
    return json_string


@app.route("/server_graph", methods=["GET"])
@authentication_required
def send_server_graph_data():

    all_data = db.get_server_graph_data()

    json_string = json.dumps(all_data)
    print(json_string)
    return json_string

# @app.route('/upload', methods=['POST'])
# @authentication_required
# def upload_file():
#     if 'file' not in request.files:
#         return jsonify({"msg": "file was not provided"}), 401
#     file = request.files['file']
#     # if user does not select file, browser also
#     # submit an empty part without filename
#     if file.filename == '':
#         return jsonify({"msg": "file has no name"}), 401

#     print(request.user)
#     file.save(os.path.join(
#         app.config['UPLOAD_FOLDER'], request.user["name"] + str(random.randint(0, 100000)) + ".json"))
#     return jsonify({"msg": "file was uploaded succesfully"}), 200
