import numpy as np
from tensorflow import keras

def convert_to_player_keras(player):
    return np.where(player>0, 0, 1)

def convert_to_action_keras(action, playerKeras):
    action_keras = np.zeros([action.shape[0],14])
    action_keras[:, action * 2 + playerKeras] = 1
    return action_keras

class ConnectFourEnvironmentKeras():

    def __init__(self, model = None, parallel_plays = 1):
        self.reward = np.repeat([[0.0, 0.0]], parallel_plays, axis=0)
        self.terminated = np.repeat([0], parallel_plays, axis=0)
        self.illegal_action = np.repeat([0], parallel_plays, axis=0)
        self.player = np.repeat([1], parallel_plays, axis=0)
        self.state = np.repeat([-np.ones(84)], parallel_plays, axis=0)
        self.valid_actions = np.repeat([[1.0, 0.0, 1.0, 0.0, 1.0, 0.0, 1.0, 0.0, 1.0, 0.0, 1.0, 0.0, 1.0, 0.0]], parallel_plays, axis=0)
        self.last_action = None
        self.logger = None
        self.verbose = False
        if model is None:
            self.model = keras.models.load_model('connect-four-environment.h5')
        else:
            self.model = model

    def copy(self):
        result = ConnectFourEnvironmentKeras(self.model)
        result.copy_from(self)
        return result

    def __str__(self):
        return self.display()

    def restart(self):
        self.__init__()

    def set_logger(self, logger):
        self.logger = logger

    def copy_from(self, env):
        self.reward = np.copy(env.reward)
        self.terminated = np.copy(env.terminated)
        self.player = np.copy(env.player)
        self.state = np.copy(env.state)
        self.valid_actions = np.copy(env.valid_actions)
        self.last_action = np.copy(env.last_action)
        self.verbose = env.verbose
        self.logger = env.logger

    def game_result(self, player, play = 0):
        return (np.where(self.reward[play, 0] > 0.5, 1, 0) - np.where(self.reward[play, 1] > 0.5, 1, 0)) * player

    def is_game_over(self, play = 0):
        return self.terminated[play] == 1

    def get_legal_actions(self, play = 0):
        playerKeras = convert_to_player_keras(self.player[play])
        free_columns = []
        for col in range(7):
            if self.valid_actions[play, col*2 + playerKeras] > 0.5:
                free_columns.append(col)
        return free_columns

    def get_player(self, play = 0):
        return self.player[play]

    def get_last_action(self, play = 0):
        if self.last_action is None:
            return None
        return self.last_action[play]

    def move(self, action):

        if len(np.shape(action)) == 0:
            action = np.array([action])

        if self.logger is not None:
            self.logger.log_before_action(self, action)

        # print("move " + str(action))
        # print(self.valid_actions)

        player_keras = convert_to_player_keras(self.player)

        # termination due to illegal action
        self.illegal_action = np.where(self.valid_actions[:, action * 2 + player_keras] > 0.5, 0, 1)
        self.terminated = np.where(self.terminated == 1, self.terminated, self.illegal_action)

        # print(action_keras)
        # print("predict")

        # exclude the the terminated plays from new prediction
        active_plays = np.nonzero(self.terminated-1)[1]
        state_active = self.state[active_plays]
        action_active = action[active_plays]
        player_keras_active =  player_keras[active_plays]

        action_keras_active = convert_to_action_keras(action_active, player_keras_active)

        [board_active, reward_active, valid_actions_active] = self.model.predict(
            [state_active, action_keras_active], batch_size=128)

        self.state[active_plays] = board_active
        self.valid_actions[active_plays] = valid_actions_active
        self.reward[active_plays] = reward_active
        # check for full boards, these plays are terminated
        self.terminated = np.where(np.amax(self.valid_actions, axis=1) < 0.5, 1, self.terminated)

        # check for positive rewards, these plays are terminated
        self.terminated = np.where(np.amax(self.reward, axis=1) > 0.5, 1, self.terminated)

        # next player
        self.player = -self.player
        self.last_action = action

        if self.logger is not None:
            self.logger.log(self)
        if self.verbose:
            print(self.display())
            print(self.get_legal_actions())
        return self

    def who_is_now(self, play=0):
        s = ""
        if self.terminated[play]:
            if self.reward[play, 0] > 0.5:
                s += "X has WON"
            elif self.reward[play, 1] > 0.5:
                s += "O has WON"
            else:
                s = "Game ended in a DRAW"
            # if self.illegal_action:
            #     s += " after illegal move"
        else:
            if self.player[play] == 1:
                s += "X"
            else:
                s += "O"
            s += " is playing now"
        return s

    def terminated_short(self, play = 0):
        if self.terminated[play]:
            return "T"
        else:
            return " "

    def reward_short(self, play = 0):
        if self.illegal_action[play] == 1:
            return "I"

        if self.reward[play, 0] > 0.5:
            return "+"

        if self.reward[play, 1] > 0.5:
            return "-"

        return " "

    def who_is_now_short(self, play=0):
        s = ""
        if self.player[play] == 1:
            s += "X"
        else:
            s += "O"
        return s

    def display(self, play=0):
        return self.display_short(cr = True, play = play) +  self.who_is_now(play) + "\n"

    def display_short(self, cr = False, play=0):
        s = ""
        for row in range(6):
            for col in range(7):
                row_offset = (14 * (5 - row))
                if self.state[play, 2 * col + row_offset] > 0:
                    s += "X"
                elif self.state[play, 2 * col + row_offset + 1] > 0:
                    s += "O"
                else:
                    s += "_"
            if cr:
                s += "\n"
        return s
