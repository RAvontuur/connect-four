from flask import Flask
from flask_cors import CORS
from environment import ConnectFourEnvironment
import sys


# https://medium.com/@onejohi/building-a-simple-rest-api-with-python-and-flask-b404371dc699
# $ export FLASK_ENV=development
# $ export FLASK_APP=app.py
# $ flask run

app = Flask(__name__)
print(sys.path)
CORS(app)

env = ConnectFourEnvironment()

def make_json(display):
    return '{"state": "' + display + '"}'

@app.route('/')
def index():
    env.restart()
    return make_json(env.display_short())

@app.route('/move/<action>')
def make_move(action):
    if env.terminated:
        env.restart()
    env.move(int(action))
    return make_json(env.display_short())