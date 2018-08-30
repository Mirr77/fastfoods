from passlib.apps import custom_app_context as pwd_hash
from db.dbsetup import open_connection
from flask import jsonify


class User(object):
    ''' User model '''

    def __init__(self, email, password, role):
        ''' Initialize user '''
        self.email = email
        self.password = password
        self.role = role

    def user_exists(self):
        """ Check if a user exists in the db """
        conn = open_connection()
        cur = conn.cursor()
        cur.execute("SELECT * from users WHERE email='{}'".format(self.email))
        user = cur.fetchone()
        cur.close()
        conn.commit()
        return user

    def user_info(self):
        """ Return user info in a dictionary """
        user = self.user_exists()

        if user:
            user_dict = {}
            user_dict['user_id'] = user[0]
            user_dict['email'] = user[1]
            user_dict['role'] = user[2]

            return user_dict

        else:
            response = jsonify({
                "message": "The user does not exist"
            })
            response.status_code = 401
            return response

    def signup(self, username):
        """ Register a new user """
        user_exists = self.user_exists()

        if user_exists:
            response = jsonify({
                "message": "An account with that email already exists"
            })
            response.status_code = 409
            return response

        else:
            hashed_pw = pwd_hash.encrypt(self.password)
            conn = open_connection()
            cur = conn.cursor()
            cur.execute("INSERT INTO users (username, email, password) VALUES('{}', '{}', '{}')"
                        .format(username, self.email, hashed_pw))
            cur.close()
            conn.commit()

            user_info = self.user_info()
            response = jsonify({
                "message": "User registered successfully",
                "user": user_info
            })
            response.status_code = 200
            return response

    def login(self):
        """ Log in existing user """
        user_exists = self.user_exists()

        if user_exists:
            pw_match = self.verify_pwd(user_exists[3])

            if pw_match:

                user_info = self.user_info()

                response = jsonify({
                    "message": "Login successful",
                    "user": user_info
                })
                response.status_code = 200
                return response

            else:
                response = jsonify({
                    "message": "Wrong password"
                })
                response.status_code = 401
                return response

        else:
            response = jsonify({
                "message": "The email you entered does not match any of our records"
            })
            response.status_code = 401
            return response

    def verify_pwd(self, stored_pwd):
        """ Confirm that the given password matches the one stored in db """
        return pwd_hash.verify(self.password, stored_pwd)

