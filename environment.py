import numpy as np

class ConnectFourEnvironment():

    ILLEGAL_MOVE_PENALTY = -1
    LOSS_PENALTY = -1
    NOT_LOSS = 0
    DRAW_REWARD = 0
    WIN_REWARD = 1


    def __init__(self):
        self.reward = 0
        self.terminated = False
        self.illegal_action = False
        self.next_to_move = 1
        self.last_action = None
        self.move_count = 0
        self.state = np.zeros(shape=(7, 6))

    def __str__(self):
        return self.display()

    def restart(self):
        self.__init__()

    def copy_from(self, env):
        self.reward = env.reward
        self.terminated = env.terminated
        self.illegal_action = env.illegal_action
        self.next_to_move = env.next_to_move
        self.last_action = env.last_action
        self.move_count = env.move_count
        self.state = env.state

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
        free_columns = []
        for col in range(7):
            if self.state[col][5] == 0:
                free_columns.append(col)
        return free_columns

    def move(self, action):
        self.last_action = action

        # Illegal move -- too high stack of squares
        if not self.state[action][5] == 0:
            return self.finish(ConnectFourEnvironment.ILLEGAL_MOVE_PENALTY, terminate=True, illegal=True)

        # Did player win
        if self.is_winning_action(self.next_to_move, action):
            self.apply_move(self.next_to_move, action)
            return self.finish(ConnectFourEnvironment.WIN_REWARD, terminate=True)

        self.apply_move(self.next_to_move, action)

        if self.all_occupied():
            return self.finish(ConnectFourEnvironment.DRAW_REWARD, terminate=True)

        return self.finish(ConnectFourEnvironment.NOT_LOSS)

    # private
    def finish(self, result, terminate = False, illegal = False):
        self.illegal_action = illegal
        self.terminated = terminate
        self.next_to_move = -self.next_to_move
        self.reward = -result
        self.move_count += 1
        return self

    # private
    def apply_move(self, next_to_move, action):

        for row in range(6):
            if self.state[action][row] == 0:
                self.state[action][row] = next_to_move
                break

    def is_winning_action(self, next_to_move, action, row_offset=0):

        for action_row in range(6):
            if self.state[action][action_row] == 0:
                break

        action_row += row_offset
        if action_row > 5:
            # illegal move
            return False

        left = 0
        right = 0
        up = 0
        down = 0
        left_up = 0
        left_down = 0
        right_up = 0
        right_down = 0

        col = action - 1
        while col >= 0:
            if self.state[col][action_row] == next_to_move:
                left += 1
                col -= 1
            else:
                break

        col = action + 1
        while col <= 6:
            if self.state[col][action_row] == next_to_move:
                right += 1
                col += 1
            else:
                break

        row = action_row - 1
        while row >= 0:
            if self.state[action][row] == next_to_move:
                down += 1
                row -= 1
            else:
                break

        col = action - 1
        row = action_row - 1
        while row >= 0 and col >= 0:
            if self.state[col][row] == next_to_move:
                left_down += 1
                col -= 1
                row -= 1
            else:
                break

        col = action + 1
        row = action_row + 1
        while row <= 5 and col <= 6:
            if self.state[col][row] == next_to_move:
                right_up += 1
                col += 1
                row += 1
            else:
                break

        col = action - 1
        row = action_row + 1
        while row <= 5 and col >= 0:
            if self.state[col][row] == next_to_move:
                left_up += 1
                col -= 1
                row += 1
            else:
                break

        col = action + 1
        row = action_row - 1
        while row >= 0 and col <= 6:
            if self.state[col][row] == next_to_move:
                right_down += 1
                col += 1
                row -= 1
            else:
                break

        if left + right + 1 >= 4:
            return True

        if up + down + 1 >= 4:
            return True

        if left_up + right_down + 1 >= 4:
            return True

        if left_down + right_up + 1 >= 4:
            return True

        return False


    def all_occupied(self):
        for col in range(7):
            if self.state[col][5] == 0:
                return False
        return True

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
        s = ""
        x = "X"
        o = "O"
        for row in range(6):
            for col in range(7):
                if self.state[col][5 - row] == 0:
                    s += "_"
                if self.state[col][5 - row] == 1:
                    s += x
                if self.state[col][5 - row] == -1:
                    s += o
            s += "\n"
        s += self.who_is_now() + "\n"
        return s

    def display_short(self):
        s = ""
        for row in range(6):
            for col in range(7):
                if self.state[col][row] == 0:
                    s += "_"
                if self.state[col][row] == 1:
                    s += "X"
                if self.state[col][row] == -1:
                    s += "O"
        return s

    def parse_state(self, s):
        self.state = np.zeros(shape=(7, 6))
        for row in range(6):
            for col in range(7):
                if s[col+(row*7)] == "X":
                    self.state[col][row] = 1
                elif s[col+(row*7)] == "O":
                    self.state[col][row] = -1

    def processState(self):
        state = self.state

        if self.next_to_move == 1:
            X = np.array([1.0, 0.0])
            O = np.array([0.0, 1.0])
        else:
            O = np.array([1.0, 0.0])
            X = np.array([0.0, 1.0])

        neural_state = np.zeros(shape=(7, 6, 2), dtype=np.float32)
        for row in range(6):
            for col in range(7):
                if state[col][row] == 1:
                    neural_state[col][row] = X
                elif state[col][row] == -1:
                    neural_state[col][row] = O

        return np.reshape([neural_state], [7 * 6 * 2]).tolist()