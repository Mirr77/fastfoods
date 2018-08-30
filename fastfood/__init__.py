from flask import Flask
from db import create_db


create_db.create_db()
app = Flask(__name__)

from fastfood.views import orders, auth, api

app.register_blueprint(api, url_prefix='/api/v1')