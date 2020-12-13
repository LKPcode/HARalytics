from functools import wraps
from flask import request
import jwt
from flask import jsonify


def encode_jwt(data):
    encoded_jwt = jwt.encode(data, 'secret', algorithm='HS256')
    return encoded_jwt


def decode_jwt(encoded_jwt):
    decoded_jwt = jwt.decode(encoded_jwt, 'secret', algorithms=['HS256'])
    return decoded_jwt


def authentication_required(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        if bearer := request.headers.get("Authorization"):
            try:
                token = bearer.split(" ")[1]
                print(token)
                request.user = decode_jwt(str.encode(token))
                return fn(*args, **kwargs)
            except Exception as e:
                print(e)
                return jsonify({"msg": "Token was not valid"}), 401
        else:
            return jsonify({"msg": "Token was not provided"}), 401
    return wrapper


# print(decode_jwt(str.encode("eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJlbWFpbCI6InNpbXBsZWFub25AdHV0YW5vdGEuY29tIiwibmFtZSI6Im5pa29zIiwicGFzc3dvcmQiOiJMb3VrYXMhQCM0IiwicGFzc3dvcmRfMiI6IkxvdWthcyFAIzQiLCJpcCI6IjEyNy4wLjAuMSIsImlzcCI6IldpbmQifQ.gKQNlcQngPwlcSMeHm8IKpbqnymYILi8jNgc3Hgw_5Y")))
