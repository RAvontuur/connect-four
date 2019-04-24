import copy
import numpy as np
import tensorflow as tf

class Player_DNN_Regressor:

    def __init__(self):
        board_column_def = tf.feature_column.numeric_column('board', shape=84)
        self.model = tf.estimator.DNNRegressor(feature_columns=[board_column_def], hidden_units=[1024, 512, 256], model_dir='dnn-regressor')


    def play(self, env, untried_actions=None):
        assert(env.terminated == False)

        if untried_actions==None:
            actions = env.get_legal_actions()
        else:
            actions = untried_actions

        boards = []
        for action in actions:
            env_next = copy.deepcopy(env)
            env_next.move(action)
            board = env_next.processState()
            boards.append(board)


        def predict_input_fn():
            features = {"board": boards}
            dataset = tf.data.Dataset.from_tensor_slices((dict(features)))
            return dataset.repeat().batch(1)


        predictions = self.model.predict(predict_input_fn)

        predicted_values = np.zeros(shape=(len(boards)), dtype=np.float32)
        for i in range(len(boards)):
            predicted_values[i] = -next(predictions)["predictions"][0]

        # print(actions)
        # print(predicted_values)

        action = actions[np.argmax(predicted_values)]

        return env.move(action), action
