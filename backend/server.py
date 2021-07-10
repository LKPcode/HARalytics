import random
from flask import Flask, url_for, jsonify
from auth import *
from werkzeug.utils import secure_filename
import os
import json
from flask_cors import CORS

from database import MySQL

app = Flask(__name__)

app.config['UPLOAD_FOLDER'] = "./uploads"
db = MySQL()
CORS(app)
#url_for('static', filename='style.css')


@app.route('/signin', methods=['POST'])
def signin():
    user = request.json
    user["ip"] = "1.1.1.1"  # request.remote_addr
    user["isp"] = "Wind"
    user["admin"] = 0
    db_user = db.user_exists(user)
    if db_user is None :
        db.create_user(user)
        return jsonify({"token": encode_jwt(user).decode("utf-8")}), 201
    else:
        return jsonify({"msg": "user already exists"}), 401



@app.route('/login', methods=['POST'])
def login():
    user = request.json
   
    # if user validates in database
    db_user = db.user_exists(user) 
    print(db_user)
    if db_user is not None:
        state = "user" if db_user["admin"]==0 else "admin" 
        return jsonify({"token": encode_jwt(db_user).decode("utf-8"), "user": db_user["username"], "state": state }), 201
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
@authentication_required(False)
def send_heatmap_data():

    data = db.get_heatmap_data_of_user(request.user["email"])

    new_structure = []
    for row in data:
        new_structure.append([row["x"], row["y"], 1.0])

    json_string = json.dumps(new_structure)
    print(json_string)
    return json_string


@app.route("/server_graph", methods=["GET"])
@authentication_required(True)
def send_server_graph_data():

    all_data = db.get_server_graph_data()

    json_string = json.dumps(all_data)
    # print(json_string)
    return json_string


@app.route("/methods", methods=["GET"])
@authentication_required(True)
def entries_per_method():
    db = MySQL()

    data = db.entries_per_method()

    data = {"methods": [method["method"] for method in data], "amounts": [method["entries"] for method in data]}

    json_string = json.dumps(data)
    # print(json_string)
    return json_string


@app.route("/status", methods=["GET"])
@authentication_required(True)
def entries_per_status():
    db = MySQL()

    data = db.entries_per_status()
    print(data)
    data = {"statuses": [method["status"] for method in data], "entries": [method["entries"] for method in data]}

    json_string = json.dumps(data)
    print(json_string)
    return json_string


@app.route("/content-type", methods=["GET"])
@authentication_required(True)
def avg_entry_age_per_type():
    db = MySQL()

    data = db.avg_entry_age_per_type()
    # print(data)
    data = {"types": [method["content_type"] for method in data], "entries": [method["average_object_age"] for method in data]}

    json_string = json.dumps(data)
    # print(json_string)
    return json_string


@app.route("/general", methods=["GET"])
@authentication_required(True)
def admin_general():
    db = MySQL()

    data = {}
    data["count_users"] = db.count_users()
    data["count_domains"] = db.count_domains()
    data["count_providers"] = db.count_providers() 

    # print(data)
    json_string = json.dumps(data)
    # print(json_string)
    return json_string


@app.route("/timings", methods=["POST"])
# @authentication_required(True)
def request_timings():
    print(request.json)

     #if values are empty -> default to all
     # Creating this structure: ["","image/png,image/jpeg","tuesday,saturday","GET",1,0,0,0]
    args = change_structure([request.json["isps"]["value"],request.json["content_types"]["value"],request.json["weekdays"]["value"], request.json["methods"]["value"]])

    print(args)

    db = MySQL()
    data= db.request_timings( args)#request.json["args"])
   
    json_string = json.dumps(data)
    print(json_string)
    return json_string


@app.route("/header-analytics", methods=["POST"])
# @authentication_required(True)
def header_analysis():
    
    print("HEADERS:", request.json)
    args = change_structure([request.json["content_types"]["value"], request.json["isps"]["value"]])

    db = MySQL()

    data = {}
    ttl = db.ttl(args)
    print(ttl)
    data["ttl"] = {}
    data["ttl"]["amount"] = [x["plhthos"] for x in ttl]
    data["ttl"]["age"] = [x["max-age"] for x in ttl]

    data["max_min"] = db.max_staled_or_min_fresh(args)
    data["cacheability"] = db.cacheability(args)

    print("ARGS",args)
    print(data)
    json_string = json.dumps(data)
    print(json_string)
    return json_string



@app.route("/all-options", methods=["GET"])
@authentication_required(False)
def all_options():
    db = MySQL()

    data= db.distinct_attributes()
    
    # print(data)
    json_string = json.dumps(data)
    # print(json_string)
    return json_string

def change_structure(values):

    args = []
    for arg in values:   
        if arg is None or len(arg)==0:
            args.append("")
        else:
            args.append( ",".join(arg) )

    for arg in values: 
        if arg is None or len(arg)==0: 
            args.append(0)     
        else:  
            args.append(1)

    return args

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
