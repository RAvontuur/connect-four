import numpy as np
import tensorflow as tf
import random
import math
import logging

from environment import ConnectFourEnvironment
from player_montecarlo import Player_MonteCarlo
from player_random import Player_Random

logging.getLogger().setLevel(logging.INFO)


number_of_simulations = 100000
player_rollout = Player_Random()
player1 = Player_MonteCarlo(number_of_simulations, rollout_player=player_rollout)
env = ConnectFourEnvironment()
env, action = player1.play(env)

[boards, labels, visits] = player1.get_boards_and_labels()
print("size: "+ str(len(labels)))
assert(len(labels) == len(boards))

idxs = [ index for index, item in enumerate(visits) if item > 20]
random.shuffle(idxs)
print("size relevants = " + str(len(idxs)))
idxs_sample = idxs[100:]
idxs_validation = idxs[:100]
boards_sample = [boards[i] for i in idxs_sample]
labels_sample= [labels[i] for i in idxs_sample]
boards_validation= [boards[i] for i in idxs_validation]
labels_validation= [labels[i] for i in idxs_validation]

# idxs = np.random.randint(len(boards_sel), size=1000)
# boards_sample = [boards_sel[i] for i in idxs]
# labels_sample = [labels_sel[i] for i in idxs]

# print(labels_sample)

board_column_def = tf.feature_column.numeric_column('board', shape=84)
model = tf.estimator.DNNRegressor(feature_columns=[board_column_def], hidden_units=[1024, 512, 256], model_dir='dnn-regressor')

def train_input_fn():
    features = {"board": boards_sample}
    labels = labels_sample
    return features, labels

print("train")
model.train(train_input_fn,steps=1000)



def show_predictions(labels, boards, size):
    idxs = np.random.randint(len(labels), size=size)
    boards_predict = [boards[i] for i in idxs]
    labels_predict = [labels[i] for i in idxs]

    def predict_input_fn():
        features = {"board": boards_predict}
        return features

    print("predict")
    predictions = model.predict(predict_input_fn)
    print("predictions")

    ss = 0.0
    for i in range(size):
        p = labels_predict[i]
        l = next(predictions)["predictions"][0]
        ssi = (p-l) * (p-l)
        ss += ssi
        print(str(i) + " " + str(ssi) + " " + str(p) + " " + str(l))

    print("ss="+str(math.sqrt(ss/size)))

show_predictions(labels_sample, boards_sample, 100)
show_predictions(labels_validation, boards_validation, 50)


def parse(s,next_to_move):

    if next_to_move == 1:
        X = np.array([1.0, 0.0])
        O = np.array([0.0, 1.0])
    else:
        O = np.array([1.0, 0.0])
        X = np.array([0.0, 1.0])

    neural_state = np.zeros(shape=(7, 6, 2), dtype=np.float32)
    for row in range(6):
        for col in range(7):
            if s[col+(row*7)] == "X":
                neural_state[col][row] = X
            elif s[col+(row*7)] == "O":
                neural_state[col][row] = O

    return np.reshape([neural_state], [7 * 6 * 2]).tolist()

board0 = parse("__________________________________________",  1)
board1 = parse("___X______________________________________", -1)
board2 = parse("____X_____________________________________", -1)
board3 = parse("_____X____________________________________", -1)
board4 = parse("______X___________________________________", -1)
board5 = parse("__OX______________________________________",  1)


def predict_input_fn():
    features = {"board":[board0, board1, board2, board3, board4, board5]}
    dataset = tf.data.Dataset.from_tensor_slices((dict(features)))
    return dataset.repeat().batch(1)

print("predict")
predictions = model.predict(predict_input_fn)
print("predictions")
print(next(predictions))
print(next(predictions))
print(next(predictions))
print(next(predictions))
print(next(predictions))
print(next(predictions))
