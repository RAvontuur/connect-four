import numpy as np
import copy
from tensorflow import keras

def convert_to_player_keras(player):
    if player < 0:
        return 1
    else:
        return 0

def convert_to_action_keras(action, playerKeras):
    action_keras = np.zeros(14)
    action_keras[action * 2 + playerKeras] = 1
    return action_keras

class ConnectFourEnvironmentKeras():

    ILLEGAL_MOVE_PENALTY = -1
    LOSS_PENALTY = -1
    NOT_LOSS = 0
    DRAW_REWARD = 0
    WIN_REWARD = 1


    def __init__(self, model = None):
        self.reward = 0
        self.terminated = False
        self.illegal_action = False
        self.next_to_move = 1
        self.last_action = None
        self.move_count = 0
        self.state = -np.ones(84)
        self.valid_actions = np.array([1.0, 0.0, 1.0, 0.0, 1.0, 0.0, 1.0, 0.0, 1.0, 0.0, 1.0, 0.0, 1.0, 0.0])
        self.connect_four = []
        self.connect_four_count = 0
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
        self.reward = env.reward
        self.terminated = env.terminated
        self.illegal_action = env.illegal_action
        self.next_to_move = env.next_to_move
        self.last_action = env.last_action
        self.move_count = env.move_count
        self.state = copy.deepcopy(env.state)
        self.valid_actions = copy.deepcopy(env.valid_actions)
        self.connect_four = env.connect_four
        self.connect_four_count = env.connect_four_count
        self.verbose = env.verbose

        self.logger = env.logger

    def get_game_state_short(self):
        return format(self.move_count, '02d') \
               + self.who_is_now_short() \
               + self.last_action_short() \
               + self.terminated_short() \
               + self.reward_short() \
               + self.display_short()

    def set_game_state_short(self, s):
        self.move_count = int(s[0:2])
        if s[2:3] == "X":
            self.next_to_move = 1
        else:
            self.next_to_move = -1
        if s[3:4] == " ":
            self.last_action = None
        else:
            self.last_action = int(s[3:4])
        self.terminated = s[4:5] == "T"
        self.illegal_action = s[5:6] == "I"
        if self.illegal_action:
            self.reward = 1
        elif s[5:6] == "+":
            self.reward = 1
        elif s[5:6] == "-":
            self.reward = -1
        else:
            self.reward = 0
        self.parse_state(s[6:48])

    def game_result(self, player):
        if player == self.next_to_move:
            return self.reward
        else:
            return -self.reward

    def is_game_over(self):
        return self.terminated

    def get_legal_actions(self):
        playerKeras = convert_to_player_keras(self.next_to_move)
        free_columns = []
        for col in range(7):
            if self.valid_actions[col*2 + playerKeras] > 0.5:
                free_columns.append(col)
        return free_columns

    def move(self, action):

        if self.logger is not None:
            self.logger.log_before_action(self, action)

        # print("move " + str(action))
        # print(self.valid_actions)

        playerKeras = convert_to_player_keras(self.next_to_move)

        if self.valid_actions[action * 2 + playerKeras] < 0.5:
            # print("illegal action, player " + str(playerKeras))
            return self.finish(ConnectFourEnvironmentKeras.ILLEGAL_MOVE_PENALTY, terminate=True, illegal=True)

        self.last_action = action

        action_keras = convert_to_action_keras(action, playerKeras)
        # print(action_keras)
        # print("predict")

        states = [self.state]
        actions = [action_keras]
        [boards, rewards, valid_actions] = self.model.predict([states, actions], batch_size=128)

        self.state = boards[0]
        self.valid_actions = valid_actions[0]

        if self.has_no_valid_actions():
            return self.finish(ConnectFourEnvironmentKeras.DRAW_REWARD, terminate=True)

        if rewards[0][playerKeras] > 0.5:
            return self.finish(ConnectFourEnvironmentKeras.WIN_REWARD, terminate=True)

        return self.finish(ConnectFourEnvironmentKeras.NOT_LOSS)


    # private
    def has_no_valid_actions(self):
        for i in range(14):
            if self.valid_actions[i] > 0:
                return False

        return True

    # private
    def finish(self, result, terminate = False, illegal = False):
        self.illegal_action = illegal
        self.terminated = terminate
        self.next_to_move = -self.next_to_move
        self.reward = -result
        self.move_count += 1
        if self.logger is not None:
            self.logger.log(self)
        if self.verbose:
            print(self.display())
            print(self.get_legal_actions())
        return self

    def who_is_now(self):
        s = ""
        if self.next_to_move == 1:
            s += "X"
        else:
            s += "O"

        if self.terminated:
            if self.reward == 1:
                s += " WON"
            elif self.reward == -1:
                s += " LOST"
            else:
                s = "Game ended in a DRAW"
            if self.illegal_action:
                s += " after illegal move"
        else:
            s += " is playing now"

        return s

    def terminated_short(self):
        if self.terminated:
            return "T"
        else:
            return " "

    def reward_short(self):
        if self.illegal_action:
            return "I"

        if self.reward == 0:
            return " "

        if self.reward > 0:
            return "+"
        else:
            return "-"

    def last_action_short(self):
        if self.last_action is None:
            return " "
        return format(self.last_action, '1d')

    def who_is_now_short(self):
        s = ""
        if self.next_to_move == 1:
            s += "X"
        else:
            s += "O"
        return s

    def display(self):
        return self.display_short(cr = True) +  self.who_is_now() + "\n"

    def display_short(self, cr = False):
        s = ""
        for row in range(6):
            for col in range(7):
                row_offset = (14 * (5 - row))
                if self.state[2 * col + row_offset] > 0:
                    s += "X"
                elif self.state[2 * col + row_offset + 1] > 0:
                    s += "O"
                else:
                    s += "_"
            if cr:
                s += "\n"
        return s
