from flask import Flask
from flask_cors import CORS
import sys


# https://medium.com/@onejohi/building-a-simple-rest-api-with-python-and-flask-b404371dc699
# $ export FLASK_ENV=development
# $ export FLASK_APP=app.py
# $ flask run

app = Flask(__name__)
print(sys.path)
CORS(app)

@app.route('/')
def index():
    return 'Server Works!'

@app.route('/greet')
def say_hello():
    return '{"state": "XOXXXOO XOXOXO XOXOXO XOXOXO XOXOXO XOXOXO"}'