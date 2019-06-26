import numpy as np
import tensorflow as tf
import random
import math
import logging

from environment import ConnectFourEnvironment
from play_writer import PlayWriter

logging.getLogger().setLevel(logging.INFO)

# load stored simulations
reader = PlayWriter(file_name="mcts.txt")
dict_plays = reader.read_plays()
print("size of dict: " + str(len(dict_plays)))
# reader.write_dict(dict_plays, "mcts_dict.txt")

board_lst = []
labels_lst = []
label_terminated_lst = []
visit_lst = []
weight_lst = []

env = ConnectFourEnvironment()
for item in dict_plays.items():
    visitv = item[1][0]
    terminated = item[0][4] == 'T'
    if visitv > 500:
            # or terminated:
        env.set_game_state_short(item[0])
        board = env.processState()
        labels = item[1][1:]
        board_lst.append(board)
        visit_lst.append(visitv)
        labels_lst.append(labels)
        label_terminated_lst.append(1 if terminated else 0)
        weight_lst.append(1.0)
            # 1 if terminated else math.sqrt(visitv))

with open("mcts_filtered.txt", 'w+') as fp:
    idxs = [ index for index, item in enumerate(visit_lst)]
    for idx in idxs:
        fp.write(str(visit_lst[idx])  + " " + str(weight_lst[idx]))
        for label in labels_lst[idx]:
            fp.write(" " + str(label))
        fp.write(" " + str(label_terminated_lst[idx]) + "\n")

print("size: "+ str(len(labels_lst)))
assert(len(labels_lst) == len(board_lst))

idxs = [ index for index, item in enumerate(visit_lst)]
random.shuffle(idxs)
idxs_sample = idxs
idxs_validation = idxs[:100]

# sample
board_samples = [board_lst[i] for i in idxs_sample]
labels_samples = [labels_lst[i] for i in idxs_sample]
label_terminated_samples = [label_terminated_lst[i] for i in idxs_sample]
weight_samples = [weight_lst[i] for i in idxs_sample]

# validation
board_validations = [board_lst[i] for i in idxs_validation]
labels_validations = [labels_lst[i] for i in idxs_validation]
label_terminated_validations = [label_terminated_lst[i] for i in idxs_validation]

# idxs = np.random.randint(len(boards_sel), size=1000)
# boards_sample = [boards_sel[i] for i in idxs]
# labels_sample = [labels_sel[i] for i in idxs]

# print(labels_sample)

board_column_def = tf.feature_column.numeric_column('board', shape=84)
model = tf.estimator.DNNRegressor(
    feature_columns=[board_column_def],
    # weight_column = 'weight',
    label_dimension=8,
    hidden_units=[1024, 512, 256],
    # dropout=0.5,
    model_dir='dnn-regressor')

def train_input_fn():
    features = {"board": board_samples}
    labels = tf.constant(labels_samples)
    return features, labels

# def train_input_fn():
#     features = {"board": boards_sample, "weight": weights_sample}
#     labels = tf.transpose(tf.constant([labels_sample, labels_terminated_sample]))
#     return features, labels

print("train")
model.train(train_input_fn,steps=1000)

def show_predictions(labels, labels_terminated, boards, size):
    idxs = np.random.randint(len(labels), size=size)
    # idxs = range(size)
    boards_predict = [boards[i] for i in idxs]
    labels_predict = [labels[i] for i in idxs]
    labels_terminated_predict = [labels_terminated[i] for i in idxs]

    def predict_input_fn():
        features = {"board": boards_predict}
        return features

    print("predict")
    predictions = model.predict(predict_input_fn)
    print("predictions")

    for i in range(size):
        p = labels_predict[i]
        q = labels_terminated_predict[i]
        l = next(predictions)["predictions"]
        print(str(i) + " " + str([p, q])  + " " + str(l))


show_predictions(labels_samples, label_terminated_samples,  board_samples, 100)
# show_predictions(labels_validation, boards_validation, 50)


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
board6 = parse("__OX_OX___________________________________",  1)


def predict_input_fn():
    features = {"board":[board0, board1, board2, board3, board4, board5, board6]}
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
print(next(predictions))
