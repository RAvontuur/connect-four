import numpy as np
import json
from environment import ConnectFourEnvironment
from player_montecarlo import Player_MonteCarlo
from player_random import Player_Random

ENV = None
PLAYER = None
strBucket = 'avoimagenet'

def handler(event, context):
    restore_session()

    action = event['pathParameters']['action']

    if action is None:
        start()
    elif action == "think":
        think()
    elif action == "start":
        start()
    else:
        move(int(action))

    return result_200()

def start():
    print("start")

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

def restore_session():
    global ENV
    global PLAYER

    if ENV is None:
        ENV = ConnectFourEnvironment()
        player_rollout = Player_Random()
        PLAYER = Player_MonteCarlo(10000, rollout_player=player_rollout)

def result_200():
    return {
        'statusCode': 200,
        'headers': {
            'Access-Control-Allow-Origin': '*'
        },
        'body': make_json(ENV)
    }

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
