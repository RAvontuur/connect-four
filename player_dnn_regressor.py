import copy
import numpy as np
import tensorflow as tf

class Player_DNN_Regressor:

    def __init__(self):
        board_column_def = tf.feature_column.numeric_column('board', shape=84)
        self.model = tf.estimator.DNNRegressor(
            feature_columns=[board_column_def],
            label_dimension=8,
            hidden_units=[1024, 512, 256],
            model_dir='dnn-regressor')


    def play(self, env, untried_actions=None):
        assert(env.terminated == False)

        if untried_actions==None:
            actions = env.get_legal_actions()
        else:
            actions = untried_actions

        board = env.processState()

        def predict_input_fn():
            features = {"board": [board]}
            dataset = tf.data.Dataset.from_tensor_slices((dict(features)))
            return dataset.repeat().batch(1)

        predictions = self.model.predict(predict_input_fn)

        predicted_values = next(predictions)["predictions"]

        predicted_values = predicted_values[1:]
        predicted_values = predicted_values[actions]
        # print(predicted_values)
        # print(actions)

        action = actions[np.argmax(predicted_values)]

        return env.move(action), action
