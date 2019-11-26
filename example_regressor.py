import numpy as np
import csv
import tensorflow as tf
import logging

logging.getLogger().setLevel(logging.INFO)

file_name = 'rollouts-filtered.csv'

boards_train = []
labels_train = []

with open(file_name, newline='') as csvfile:
    reader = csv.reader(csvfile, quoting=csv.QUOTE_NONNUMERIC)
    for row in reader:
        labels_train.append(row[0:2])
        boards_train.append(row[2:86])

print(len(labels_train))

board_column_def = tf.feature_column.numeric_column('board', shape=84)
model = tf.estimator.DNNRegressor(
    feature_columns=[board_column_def],
    label_dimension=2,
    hidden_units=[256, 256],
    dropout=0.05,
    model_dir='dnn-regressor')

def train_input_fn():
    features = {"board":boards_train}
    labels = labels_train
    return features, labels

print("train")
model.train(train_input_fn,steps=5000)

def show_predictions(labels, boards, size):
    idxs = np.random.randint(len(labels), size=size)
    # idxs = range(size)
    boards_predict = [boards[i] for i in idxs]
    labels_predict = [labels[i] for i in idxs]

    def predict_input_fn():
        features = {"board":boards_predict}
        dataset = tf.data.Dataset.from_tensor_slices((dict(features)))
        return dataset.repeat().batch(1)

    print("predict")
    predictions = model.predict(predict_input_fn)
    print("predictions")

    j = 0
    for i in range(size):
        p = labels_predict[i]
        l = next(predictions)["predictions"]
        print(str(i) + " " + str(p)  + " " + str(l))
        if (abs(p[0] - l[0]) < 0.5) and (abs(p[1] - l[1]) < 0.5):
            j+=1
    print(str(j) + " good predictions, out of " + str(size))


print("predictions")
show_predictions(labels_train, boards_train, 100)