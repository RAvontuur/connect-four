import numpy as np
import tensorflow as tf
import random
import math
import logging

from environment import ConnectFourEnvironment
from player_montecarlo import Player_MonteCarlo
from player_random import Player_Random

logging.getLogger().setLevel(logging.INFO)

player_rollout = Player_Random()
player1 = Player_MonteCarlo(100000, rollout_player=player_rollout)
env = ConnectFourEnvironment()
env, action = player1.play(env)

[boards, labels] = player1.get_boards_and_labels()
print("size: "+ str(len(labels)))
assert(len(labels) == len(boards))

# equiv. random.sample
idxs = np.random.randint(len(labels), size=1000)
print(idxs)
boards_sample = [boards[i] for i in idxs]
labels_sample = [labels[i] for i in idxs]

print(labels_sample)

board_column_def = tf.feature_column.numeric_column('board', shape=84)
model = tf.estimator.DNNRegressor(feature_columns=[board_column_def], hidden_units=[1024, 512, 256], dropout=0.5)

def train_input_fn():
    features = {"board": boards_sample}
    labels = labels_sample
    return features, labels

print("train")
model.train(train_input_fn,steps=500)



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
show_predictions(labels, boards, 100)
