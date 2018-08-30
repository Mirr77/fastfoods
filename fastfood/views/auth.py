''' import modules '''
import re
from flask import jsonify, request
from fastfood.views import api
from fastfood.models.auth import User
from db.dbsetup import open_connection

email_format = r"(^[a-zA-z0-9_.]+@[a-zA-z0-9-]+\.[a-z]+$)"


@api.route('auth/signup', methods=['POST'])
def sign_up():
    conn = open_connection()
    cur = conn.cursor()
    email = request.get_json('email')['email']
    password = request.get_json('password')['password']
    username = request.get_json('username')['username']
    cur.execute("select * from users where username = '{}'".format(username))
    names = cur.fetchall()
    cur.close()

    if len(names) > 0:
        response = jsonify({"message": "Username is taken"})
        response.status_code = 409
        return response

    if not email or email == " ":
        response = jsonify({"message": "Email not provided"})
        response.status_code = 400
        return response

    if not re.match(email_format, email):
        return jsonify({"message": "incorrect email format"})

    if not password or password == " ":
        response = jsonify({"message": "Password not provided"})
        response.status_code = 400
        return response

    if not username or username == " ":
        response = jsonify({"message": "Username not provided"})
        response.status_code = 400
        return response

    if not request.json:
        response = jsonify({"message": "Incorrect request format"})
        response.status_code = 400
        return response

    user = User(email, password)
    register = user.signup(username)
    return register


@api.route('/login', methods=['POST'])
def login():
    email = request.get_json('email')['email']
    password = request.get_json('password')['password']

    if not email or email == " ":
        response = jsonify({"message": "Email not provided"})
        response.status_code = 400
        return response

    if not re.match(email_format, email):
        response = jsonify({"message": "incorrect email format"})
        response.status_code = 400
        return response

    if not password or password == " ":
        response = jsonify({"message": "Password not provided"})
        response.status_code = 400
        return response

    if not request.json:
        response = jsonify({"message": "Invalid request format"})
        response.status_code = 400
        return response

    else:
        user = User(email, password)
        login = user.login()
        return login


