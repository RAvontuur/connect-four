import numpy as np
import copy

class ConnectFourEnvironment():

    ILLEGAL_MOVE_PENALTY = -1
    LOSS_PENALTY = -1
    NOT_LOSS = 0
    DRAW_REWARD = 0
    WIN_REWARD = 1


    def __init__(self):
        self.reward = ConnectFourEnvironment.NOT_LOSS
        self.terminated = False
        self.illegal_action = False
        self.player = 1
        self.last_action = None
        self.move_count = 0
        self.state = np.zeros(shape=(7, 6))
        self.connect_four = []
        self.connect_four_count = 0

    def copy(self):
        result = ConnectFourEnvironment()
        result.copy_from(self)
        return result

    def __str__(self):
        return self.display()

    def restart(self):
        self.__init__()

    def copy_from(self, env):
        self.reward = env.reward
        self.terminated = env.terminated
        self.illegal_action = env.illegal_action
        self.player = env.player
        self.last_action = env.last_action
        self.move_count = env.move_count
        self.state = copy.deepcopy(env.state)
        self.connect_four = env.connect_four
        self.connect_four_count = env.connect_four_count

    def get_player(self):
        return self.player

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
            self.player = 1
        else:
            self.player = -1
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
        if player == self.player:
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

    def get_last_action(self):
        return self.last_action

    def move(self, action):

        self.last_action = action

        # Illegal move -- too high stack of squares
        if not self.state[action][5] == 0:
            return self.finish(ConnectFourEnvironment.ILLEGAL_MOVE_PENALTY, terminate=True, illegal=True)

        # Did player win
        if self.is_winning_action(self.player, action):
            self.apply_move(self.player, action)
            return self.finish(ConnectFourEnvironment.WIN_REWARD, terminate=True)

        self.apply_move(self.player, action)

        if self.all_occupied():
            return self.finish(ConnectFourEnvironment.DRAW_REWARD, terminate=True)

        return self.finish(ConnectFourEnvironment.NOT_LOSS)

    # private
    def finish(self, result, terminate = False, illegal = False):
        self.illegal_action = illegal
        self.terminated = terminate
        self.player = -self.player
        self.reward = -result
        self.move_count += 1
        return self

    # private
    def apply_move(self, player, action):

        for row in range(6):
            if self.state[action][row] == 0:
                self.state[action][row] = player
                break

    def is_winning_action(self, player, action, row_offset=0):

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
            if self.state[col][action_row] == player:
                left += 1
                col -= 1
            else:
                break

        col = action + 1
        while col <= 6:
            if self.state[col][action_row] == player:
                right += 1
                col += 1
            else:
                break

        row = action_row - 1
        while row >= 0:
            if self.state[action][row] == player:
                down += 1
                row -= 1
            else:
                break

        col = action - 1
        row = action_row - 1
        while row >= 0 and col >= 0:
            if self.state[col][row] == player:
                left_down += 1
                col -= 1
                row -= 1
            else:
                break

        col = action + 1
        row = action_row + 1
        while row <= 5 and col <= 6:
            if self.state[col][row] == player:
                right_up += 1
                col += 1
                row += 1
            else:
                break

        col = action - 1
        row = action_row + 1
        while row <= 5 and col >= 0:
            if self.state[col][row] == player:
                left_up += 1
                col -= 1
                row += 1
            else:
                break

        col = action + 1
        row = action_row - 1
        while row >= 0 and col <= 6:
            if self.state[col][row] == player:
                right_down += 1
                col += 1
                row -= 1
            else:
                break

        self.connect_four = []
        if left + right + 1 >= 4:
            left_pos = action - left + (7 * action_row)
            self.connect_four.append(left_pos)
            self.connect_four.append(left_pos + 1)
            self.connect_four.append(left_pos + 2)
            self.connect_four.append(left_pos + 3)
            self.connect_four_count+=1
            if left + right + 1 >= 5:
                self.connect_four_count+=1
                self.connect_four.append(left_pos + 4)
            if left + right + 1 >= 6:
                self.connect_four_count+=1
                self.connect_four.append(left_pos + 5)
            if left + right + 1 >= 7:
                self.connect_four_count+=1
                self.connect_four.append(left_pos + 6)

        if up + down + 1 >= 4:
            down_pos = action + (7 * (action_row - down))
            self.connect_four.append(down_pos)
            self.connect_four.append(down_pos + 7)
            self.connect_four.append(down_pos + 14)
            self.connect_four.append(down_pos + 21)
            self.connect_four_count+=1

        if left_up + right_down + 1 >= 4:
            right_down_pos = action + right_down + (7 * (action_row - right_down))
            self.connect_four.append(right_down_pos)
            self.connect_four.append(right_down_pos + 6)
            self.connect_four.append(right_down_pos + 12)
            self.connect_four.append(right_down_pos + 18)
            self.connect_four_count+=1
            if left_up + right_down + 1 >= 5:
                self.connect_four.append(right_down_pos + 24)
                self.connect_four_count+=1
            if left_up + right_down + 1 >= 6:
                self.connect_four.append(right_down_pos + 30)
                self.connect_four_count+=1

        if left_down + right_up + 1 >= 4:
            left_down_pos = action - left_down + (7 * (action_row - left_down))
            self.connect_four.append(left_down_pos)
            self.connect_four.append(left_down_pos + 8)
            self.connect_four.append(left_down_pos + 16)
            self.connect_four.append(left_down_pos + 24)
            self.connect_four_count+=1
            if left_down + right_up + 1 >= 5:
                self.connect_four.append(left_down_pos + 32)
                self.connect_four_count+=1
            if left_down + right_up + 1 >= 6:
                self.connect_four.append(left_down_pos + 40)
                self.connect_four_count+=1

        return self.connect_four_count > 0


    def all_occupied(self):
        for col in range(7):
            if self.state[col][5] == 0:
                return False
        return True

    def who_is_now(self):
        s = ""
        if self.player == 1:
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
        if self.player == 1:
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

    def display_csv(self):
        s = ""
        for row in range(6):
            for col in range(7):
                if self.state[col][row] == 0:
                    s += ", -1, -1"
                if self.state[col][row] == 1:
                    s += ", 1, -1"
                if self.state[col][row] == -1:
                    s += ", -1, 1"
        return s[2:]

    def parse_state(self, s):
        self.state = np.zeros(shape=(7, 6))
        for row in range(6):
            for col in range(7):
                if s[col+(row*7)] == "X":
                    self.state[col][row] = 1
                elif s[col+(row*7)] == "O":
                    self.state[col][row] = -1
