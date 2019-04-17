import numpy as np
import tensorflow as tf


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


board1 = parse("__________________________________________", 1)
label1 = 0.2
board2 = parse("___X______________________________________", -1)
label2 = -0.2
board3 = parse("X_________________________________________", -1)
label3 = 0.05
board4 = parse("____X_____________________________________", -1)
label4 = 0.1

print([board1, board2, board3, board4])


board_column_def = tf.feature_column.numeric_column('board', shape=84)
model = tf.estimator.DNNRegressor(feature_columns=[board_column_def], hidden_units=[1024, 512, 256])

def train_input_fn():
    features = {"board":[board1, board2, board3, board4]}
    labels = [label1, label2, label3, label4]
    return features, labels

print("train")
model.train(train_input_fn,steps=100)

def predict_input_fn():
    features = {"board":[board1, board2, board3, board4]}
    return features

print("predict")
predictions = model.predict(predict_input_fn)
print("predictions")
print(next(predictions))
print(next(predictions))
print(next(predictions))
print(next(predictions))