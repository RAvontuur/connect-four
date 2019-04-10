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

    return np.reshape([neural_state], [7 * 6 * 2])

print(parse("O_XXX____OOX______O_______________________", 1))
print(parse("O_XXX____OOX______O_______________________", -1))


board = tf.feature_column.numeric_column('board', shape=4)


featcols = [board]

model = tf.estimator.DNNRegressor(feature_columns=featcols, hidden_units=[1024, 512, 256])

def train_input_fn():
    features = {"board":[[0,0,0,0],[1,0,1,0], [0,1,0,1]]}
    labels = [ 0, 1, -1 ]
    return features, labels

print("train")
model.train(train_input_fn,steps=100)

def predict_input_fn():
    features = {"board":[[0,0,0,0], [1,0,1,0], [0,1,0,0]]}
    return features

print("predict")
predictions = model.predict(predict_input_fn)
print("predictions")
print(next(predictions))
print(next(predictions))
print(next(predictions))