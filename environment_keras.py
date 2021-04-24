import numpy as np
from tensorflow import keras
import time


def convert_to_player_keras(player):
    return np.where(player>0, 0, 1)


def convert_to_action_keras(action, playerKeras):
    action_keras = np.zeros([action.shape[0],14])
    action_keras[range(action.shape[0]), action * 2 + playerKeras] = 1
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
        self.timer1 = 0
        if model is None:
            self.model = keras.models.load_model('connect-four-environment.h5')
        else:
            self.model = model
        # self.counterOK = 0
        # self.counterNOK = 0
        self.ignore_invalid_actions = True

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
        else:
            action = np.array(action)

        if self.logger is not None:
            self.logger.log_before_action(self, action)

        # exclude the the terminated plays from new prediction
        active_plays = np.nonzero(self.terminated-1)

        player_keras = convert_to_player_keras(self.player)

        # termination due to illegal action
        indices_tuple = (range(action.shape[0]), action * 2 + player_keras)
        valid_action_indices = self.valid_actions[indices_tuple]
        self.illegal_action[active_plays] = np.where(valid_action_indices[active_plays] > 0.5, 0, 1)

        if not self.ignore_invalid_actions:
            if np.any(self.illegal_action[active_plays] == 1):
                # print("action * 2 + player_keras: {}".format(action * 2 + player_keras))
                # print("valid actions indices {}:".format(valid_action_indices.shape))
                # print(valid_action_indices)
                illegal_action_plays = []
                for play in active_plays[0]:
                    if self.illegal_action[play] == 1:
                        illegal_action_plays.append(play)
                        if self.get_player(play) == 1:
                            self.reward[active_plays, 1] = 1
                        else:
                            self.reward[active_plays, 0] = 1

        # print("terminated {} game(s) due to illegal action: {}".format(len(illegal_action_plays), illegal_action_plays))

        # for play in active_plays[0]:
        #     print(self.display(play))
        #     print("action {} on play {}".format(action[play], play))
        #     print("with valid actions: {}".format(self.valid_actions[play]))
        #     print("action * 2 + player_keras: {}".format((action * 2 + player_keras)[play]))
        #     print("valid actions indices {}:".format(valid_action_indices[play]))

        self.terminated = np.where(self.terminated == 1, 1, self.illegal_action)
        if np.all(self.terminated == 1):
            return self

        active_plays = np.nonzero(self.terminated-1)
        state_active = self.state[active_plays]
        action_active = action[active_plays]
        player_keras_active =  player_keras[active_plays]
        action_keras_active = convert_to_action_keras(action_active, player_keras_active)

        begin1 = time.time()
        [board_active, reward_active, valid_actions_active] = self.model.predict(
            [state_active, action_keras_active], batch_size=128)
        self.timer1 += time.time() - begin1

        self.state[active_plays] = board_active
        self.valid_actions[active_plays] = valid_actions_active
        self.reward[active_plays] = reward_active

        # verify no valid actions current player
        # for play in active_plays[0]:
        #     offset = 0
        #     if self.player[play] < 0:
        #         offset = 1
        #     failed = False
        #     for i in range(7):
        #         if self.valid_actions[play][i*2 + offset] > 0.5:
        #             print("play {} is corrupt for {} and valid_actions {}".format(play, i*2 + offset, self.valid_actions[play] ))
        #             failed = True
        #             break
        #     if failed:
        #         self.counterNOK += 1
        #     else:
        #         self.counterOK += 1

        # check for full boards, these plays are terminated
        self.terminated = np.where(self.terminated == 1, 1, np.amax(self.valid_actions, axis=1) < 0.5)

        # check for positive rewards, these plays are terminated
        self.terminated = np.where(self.terminated == 1, 1, np.amax(self.reward, axis=1) > 0.5)

        if self.last_action is None:
            self.last_action = action
        else:
            self.last_action[active_plays] = action[active_plays]
        active_plays = np.nonzero(self.terminated-1)
        self.player[active_plays] = -self.player[active_plays]

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
            elif self.illegal_action[play] == 1:
                if self.player[play] == 1:
                    s += "X has LOST after illegal move"
                else:
                    s += "O has LOST after illegal move"
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