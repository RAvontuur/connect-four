import collections
import copy
import numpy as np

class Environment:

    def __init__(self, state_shape, n_actions, state_dtype=None):
        self.state_shape = state_shape
        self.n_actions = n_actions
        if state_dtype is None:
            # Assume all arrays are float32.
            if isinstance(state_shape[0], collections.Sequence):
                self.state_dtype = [np.float32] * len(state_shape)
            else:
                self.state_dtype = np.float32
        else:
            self.state_dtype = state_dtype

    def game_result(self):
        raise NotImplemented("Implement game_result function")

    def is_game_over(self):
        raise NotImplemented("Implement is_game_over function")

    def move(self, action):
        raise NotImplemented("Implement move function")

    def get_legal_actions(self):
        raise NotImplemented("Implement get_legal_actions function")


class ConnectFourEnvironment(Environment):
    X = np.array([1.0, 0.0])
    O = np.array([0.0, 1.0])
    EMPTY = np.array([0.0, 0.0])

    def __init__(self):
        super(ConnectFourEnvironment, self).__init__([(7, 6, 2)], 7)
        self.actions = 7
        self.ILLEGAL_MOVE_PENALTY = -1
        self.LOSS_PENALTY = -1
        self.NOT_LOSS = 0
        self.DRAW_REWARD = 0
        self.WIN_REWARD = 1
        self.reward = 0
        self.terminated = False
        self.illegal_action = False
        self.next_to_move = 1
        self.state = [np.zeros(shape=(7, 6, 2), dtype=np.float32)]

    def __str__(self):
        return self.display()

    def game_result(self):
        return self.reward

    def is_game_over(self):
        return self.terminated

    def get_legal_actions(self):
        return [0, 1, 2, 3, 4, 5, 6]

    def move(self, action):
        self.reward = self.step(action)

        next = copy.deepcopy(self)
        next.next_to_move = -next.next_to_move
        next.reward = -next.reward
        return next

    def step(self, action):
        # Illegal move -- too high stack of squares
        if not np.all(self.state[0][action][5] == ConnectFourEnvironment.EMPTY):
            self.terminated = True
            self.illegal_action = True
            return self.ILLEGAL_MOVE_PENALTY

        if self.next_to_move == 1:
            player = ConnectFourEnvironment.X
        else:
            player = ConnectFourEnvironment.O

        self.apply_move(player, action)

        # Did player win
        if self.check_winner(player, action):
            self.terminated = True
            return self.WIN_REWARD

        if self.game_over():
            self.terminated = True
            return self.DRAW_REWARD

        return self.NOT_LOSS

    def apply_move(self, player, action):
        for row in range(6):
            if np.all(self.state[0][action][row] == ConnectFourEnvironment.EMPTY):
                self.state[0][action][row] = player
                break

    def check_winner(self, player, action):

        for row in range(6):
            if np.all(self.state[0][action][5 - row] == player):
                action_row = 5 - row
                break

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
            if np.all(self.state[0][col][action_row] == player):
                left = left + 1
                col = col - 1
            else:
                break

        col = action + 1
        while col <= 6:
            if np.all(self.state[0][col][action_row] == player):
                right = right + 1
                col = col + 1
            else:
                break

        row = action_row - 1
        while row >= 0:
            if np.all(self.state[0][action][row] == player):
                down = down + 1
                row = row - 1
            else:
                break

        row = action_row + 1
        while row <= 5:
            if np.all(self.state[0][action][row] == player):
                up = up + 1
                row = row + 1
            else:
                break

        col = action - 1
        row = action_row - 1
        while row >= 0 and col >= 0:
            if np.all(self.state[0][col][row] == player):
                left_down = left_down + 1
                col = col - 1
                row = row - 1
            else:
                break

        col = action + 1
        row = action_row + 1
        while row <= 5 and col <= 6:
            if np.all(self.state[0][col][row] == player):
                right_up = right_up + 1
                col = col + 1
                row = row + 1
            else:
                break

        col = action - 1
        row = action_row + 1
        while row <= 5 and col >= 0:
            if np.all(self.state[0][col][row] == player):
                left_up = left_up + 1
                col = col - 1
                row = row + 1
            else:
                break

        col = action + 1
        row = action_row - 1
        while row >= 0 and col <= 6:
            if np.all(self.state[0][col][row] == player):
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


    def game_over(self):
        for col in range(7):
            if np.all(self.state[0][col][5] == ConnectFourEnvironment.EMPTY):
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
                s += " after illegal move previous player"
        else:
            s += " is playing now"

        return s

    def display(self):
        state = self.state[0]
        s = ""
        x = "X"
        o = "O"
        for row in range(6):
            for col in range(7):
                if np.all(state[col][5 - row] == ConnectFourEnvironment.EMPTY):
                    s += "_"
                if np.all(state[col][5 - row] == ConnectFourEnvironment.X):
                    s += x
                if np.all(state[col][5 - row] == ConnectFourEnvironment.O):
                    s += o
            s += "\n"
        s += self.who_is_now() + "\n"
        return s
