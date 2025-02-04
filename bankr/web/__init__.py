from flask import Flask
from flask_cors import CORS


app = Flask('bankr')
app.config['ENV'] = 'development'
app.config['DEBUG'] = True

CORS(app, resources={r"*": {"origins": "*"}}, supports_credentials=True)

from . import auth
from . import api
