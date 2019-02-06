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
        self.state = None
        # self.state = [np.zeros(shape=(7, 6, 2), dtype=np.float32)]

    def __str__(self):
        return self.display()

    # def __deepcopy__(self, memodict={}):
    #     copy_object = ConnectFourEnvironment()
    #     copy_object.reward = self.reward
    #     copy_object.terminated = self.terminated
    #     copy_object.illegal_action = self.illegal_action
    #     copy_object.next_to_move = self.next_to_move
    #     copy_object.state = np.copy(self.state)
    #
    #     return copy_object

    def reset_board(self):
        self.state = np.zeros(shape=(7, 6))

    def game_result(self, player):
        if player == self.next_to_move:
            return self.reward
        else:
            return -self.reward

    def is_game_over(self):
        return self.terminated

    def get_legal_actions(self):
        return [0, 1, 2, 3, 4, 5, 6]

    def move(self, action):
        self.reward = self.step(action)
        return self

    def step(self, action):
        # Illegal move -- too high stack of squares
        if not self.state[action][5] == 0:
            self.terminated = True
            self.illegal_action = True
            return ConnectFourEnvironment.ILLEGAL_MOVE_PENALTY



        # Did player win
        if self.is_winning_action(self.next_to_move, action):
            self.apply_move(self.next_to_move, action)
            self.terminated = True
            return ConnectFourEnvironment.WIN_REWARD

        self.apply_move(self.next_to_move, action)

        if self.all_occupied():
            self.terminated = True
            return ConnectFourEnvironment.DRAW_REWARD

        self.next_to_move = -self.next_to_move
        return ConnectFourEnvironment.NOT_LOSS

    def apply_move(self, next_to_move, action):

        for row in range(6):
            if self.state[action][row] == 0:
                self.state[action][row] = self.next_to_move
                break

    def is_winning_action(self, next_to_move, action, row_offset=0):

        action_row = 0
        for row in range(5):
            action_row = 5 - row
            if not self.state[action][action_row - 1] == 0:
                break

        action_row += row_offset
        if action_row > 5:
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
                left = left + 1
                col = col - 1
            else:
                break

        col = action + 1
        while col <= 6:
            if self.state[col][action_row] == next_to_move:
                right = right + 1
                col = col + 1
            else:
                break

        row = action_row - 1
        while row >= 0:
            if self.state[action][row] == next_to_move:
                down = down + 1
                row = row - 1
            else:
                break

        col = action - 1
        row = action_row - 1
        while row >= 0 and col >= 0:
            if self.state[col][row] == next_to_move:
                left_down = left_down + 1
                col = col - 1
                row = row - 1
            else:
                break

        col = action + 1
        row = action_row + 1
        while row <= 5 and col <= 6:
            if self.state[col][row] == next_to_move:
                right_up = right_up + 1
                col = col + 1
                row = row + 1
            else:
                break

        col = action - 1
        row = action_row + 1
        while row <= 5 and col >= 0:
            if self.state[col][row] == next_to_move:
                left_up = left_up + 1
                col = col - 1
                row = row + 1
            else:
                break

        col = action + 1
        row = action_row - 1
        while row >= 0 and col <= 6:
            if self.state[col][row] == next_to_move:
                right_down = right_down + 1
                col = col + 1
                row = row - 1
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
