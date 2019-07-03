import numpy as np
import json
from environment import ConnectFourEnvironment
from player_montecarlo import Player_MonteCarlo
from player_random import Player_Random
from dynamo_repository import DynamoRepository

ENV = None
PLAYER = None
DYNAMO = None
strBucket = 'avoimagenet'

def handler(event, context):
    initialize()

    action = event['pathParameters']['action']

    if action is None:
        start()
        return result_200(None)

    actions = action.split("-")
    if len(actions) < 2:
        start()
        return result_200(None)

    action = actions[0]
    play_id = actions[1]

    restore_session(play_id)

    if action == "think":
        think()
    elif action == "start":
        start()
    else:
        move(int(action))

    return result_200(play_id)

def start():
    print("restart")
    ENV.restart()

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

def initialize():
    global ENV
    global PLAYER
    global DYNAMO

    if DYNAMO is None:
        DYNAMO = DynamoRepository()
        ENV = ConnectFourEnvironment()
        player_rollout = Player_Random()
        PLAYER = Player_MonteCarlo(10000, rollout_player=player_rollout)

def restore_session(play_id):

    print("restore session %s" % (play_id))

    state = DYNAMO.read_play(play_id)
    print("retrieved state %s" % (state))

    ENV.set_game_state_short(state)

def result_200(play_id):

    if play_id is None:
        play_id = str(np.random.randint(99999999))

    DYNAMO.update_play(play_id, ENV.get_game_state_short())

    return {
        'statusCode': 200,
        'headers': {
            'Access-Control-Allow-Origin': '*'
        },
        'body': make_json(ENV, play_id)
    }

def make_json(env, play_id):
    x = {}
    x["state"] = env.display_short()
    x["msg"] = who_is_now(env)
    x["terminated"] = env.terminated
    x["connect_four"] = env.connect_four
    x["playId"] = play_id
    return json.dumps(x)

def who_is_now(env):
    s = ""
    if env.next_to_move == 1:
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

    return s
