import argparse
import json
import numpy as np

from flask import Flask, jsonify
from flask_cors import CORS

from environment import ConnectFourEnvironment
from player_montecarlo import PlayerMonteCarlo
from player_random import PlayerRandom

print("Starting app.py")

app = Flask(__name__, instance_path="/{project_folder_abs_path}")
CORS(app, resources=r'/play/*')

ENV = ConnectFourEnvironment()
player_rollout = PlayerRandom()
PLAYER = PlayerMonteCarlo(10000, rollout_player=player_rollout)


@app.route('/play/start')
def start():
    print("restart")
    ENV.restart()

    return jsonify(result_200(None, "start"))


@app.route('/play/<path:action>-<path:play_id>')
def play(action, play_id):
    print(str(action) + " " + str(play_id))

    if action == "think":
        think()
    elif action == "start":
        start()
    else:
        move(int(action))

    return result_200(play_id, action)


def move(action):
    print("move %s" % (str(action)))
    if ENV.terminated:
        ENV.restart()
    ENV.move(action)


def think():
    print("think")
    if not ENV.terminated:
        env2, action = PLAYER.play(ENV)
        ENV.copy_from(env2)
        print("visits: " + str(PLAYER.visits()))


def result_200(play_id, action):
    if play_id is None:
        play_id = str(np.random.randint(99999999))

    return make_json(ENV, PLAYER, play_id, action)


def make_json(env, player, play_id, action):
    x = {"state": env.display_short(), "msg": who_is_now(env, player, action), "terminated": env.terminated,
         "connect_four": env.connect_four, "playId": play_id}

    if action == "think":
        x["choices"] = player.choices()
        x["visits"] = player.visits()
        x["analyzed_result"] = player.analyzed_result()
    return x


def who_is_now(env, player, action):
    s = ""
    if env.get_player() == 1:
        s += "RED"
    else:
        s += "YELLOW"

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
        if action == "think" and player.analyzed_result() is not None:
            if player.analyzed_result() == 1:
                s += " (YELLOW wins)"
            else:
                s += " (RED wins)"
    return s


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Endpoint for d3 connect-four')
    parser.add_argument('-p', '--port', dest='port', help='Port number', default=8081)

    args = parser.parse_args()
    port = args.port

    app.run(host="0.0.0.0", port=port, debug=False, threaded=True)
