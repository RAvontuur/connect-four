from flask import Flask
from flask_cors import CORS
from environment import ConnectFourEnvironment
from player_montecarlo import Player_MonteCarlo
from player_random import Player_Random
import sys
import json


# https://medium.com/@onejohi/building-a-simple-rest-api-with-python-and-flask-b404371dc699
# $ source venv/bin/activate
# $ export FLASK_ENV=development
# $ export FLASK_APP=app.py
# $ flask run

app = Flask(__name__)
print(sys.path)
CORS(app)

env = ConnectFourEnvironment()
player_rollout = Player_Random()
player1 = Player_MonteCarlo(10000, rollout_player=player_rollout)

def make_json(env):
    x = {}
    x["state"] = env.display_short()
    x["msg"] = who_is_now(env)
    x["terminated"] = env.terminated
    return json.dumps(x)

def who_is_now(env):
    s = ""
    if env.next_to_move == 1:
        s += "X"
    else:
        s += "O"

    if env.terminated:
        if env.reward == 1:
            s += " WON"
        elif env.reward == -1:
            s += " LOST"
        else:
            s = "Game ended in a DRAW"
        if env.illegal_action:
            s += " after illegal move"
    else:
        s += " is playing now"

    return s

@app.route('/')
def index():
    return make_json(env)

@app.route('/restart')
def restart():
    env.restart()
    return make_json(env)

@app.route('/think')
def think():
    if not env.terminated:
        env2, action = player1.play(env)
        env.copy_from(env2)
    return make_json(env)

@app.route('/move/<action>')
def make_move(action):
    if env.terminated:
        env.restart()
    env.move(int(action))
    return make_json(env)