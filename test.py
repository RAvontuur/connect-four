import math
import numpy as np
import tensorflow as tf


board_column_def = tf.feature_column.numeric_column('board', shape=84)
model = tf.estimator.DNNRegressor(feature_columns=[board_column_def], hidden_units=[1024, 512, 256], model_dir='dnn-regressor')

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