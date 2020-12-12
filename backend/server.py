
import random
from flask import Flask, url_for, jsonify
from auth import *
from werkzeug.utils import secure_filename
import os

from database import MongoDB

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = "./uploads"
db = MongoDB()


# url_for('static', filename='style.css')


@app.route('/signin', methods=['POST'])
def signin():
    user = request.json
    if db.create_user(user):
        return jsonify({"token": encode_jwt(user).decode("utf-8")}), 201
    else:
        return jsonify({"msg": "user already exists"}), 401


@app.route('/login', methods=['POST'])
def login():
    user = request.json
    # if user validates in database
    if db.user_exists(user):
        return jsonify({"token": encode_jwt(user).decode("utf-8")}), 201
    else:
        return jsonify({"msg": "user credentials are not correct"}), 401


@app.route("/upload", methods=["POST"])
# @authentication_required
def upload_data():
    data = request.json
    print(data["new_json"][0])
    try:
        #db.insert_entries(request.user, data["new_json"])
        return jsonify({"msg": "upload was succesfull"}), 200
    except:
        return jsonify({"msg": "JSON data does not have the right structure"}), 404

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
