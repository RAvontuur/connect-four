import collections
import copy
import numpy as np
import random

from mcts.common import TwoPlayersGameState


class Environment(TwoPlayersGameState):
    """An environment in which an actor performs actions to accomplish a task.

    An environment has a current state, which is represented as either a single NumPy
    array, or optionally a list of NumPy arrays.  When an action is taken, that causes
    the state to be updated.  Exactly what is meant by an "action" is defined by each
    subclass.  As far as this interface is concerned, it is simply an arbitrary object.
    The environment also computes a reward for each action, and reports when the task
    has been terminated (meaning that no more actions may be taken).
    """

    def __init__(self, state_shape, n_actions, state_dtype=None):
        """Subclasses should call the superclass constructor in addition to doing their own initialization."""
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


class ConnectFourEnvironment(Environment):
    """
    Play Connect Four against a randomly acting opponent
    """
    X = np.array([1.0, 0.0])
    O = np.array([0.0, 1.0])
    EMPTY = np.array([0.0, 0.0])

    def __init__(self):
        super(ConnectFourEnvironment, self).__init__([(7, 6, 2)], 7)
        self.actions = 7
        self.play_level = 100
        self.reset()
        self.ILLEGAL_MOVE_PENALTY = -1.0
        self.LOSS_PENALTY = -1.0
        self.NOT_LOSS = 0.0
        self.DRAW_REWARD = 0.0
        self.WIN_REWARD = 1.0

    def __str__(self):
        return self.display()

    def game_result(self):
        return self._game_result

    def is_game_over(self):
        return self.terminated

    def move(self, action):
        next_env = copy.deepcopy(self)
        next_env.step(action)
        return next_env

    def get_legal_actions(self):
        return [0,1,2,3,4,5,6]

    def set_play_level(self, level):
        # -3: inverts state
        # -2: inverts state + pause
        # -1: manual play mode
        #  0: random play
        #  1: makes 4 if possible, otherwise random play
        #  2: makes 4 and prevents 4 if possible, otherwise random
        self.play_level = level

    def reset(self):
        self.terminated = False
        self.reverted = False
        self.next_to_move = 0
        self.state = [np.zeros(shape=(7, 6, 2), dtype=np.float32)]

        # Randomize who goes first
        if random.randint(0, 1) == 1:
            self.make_O_action()

    def who_is_now(self):
        if self.reverted:
            if self.play_level == -1:
                return 'I'
            else:
                return 'TRAINER'
        else:
            if self.play_level == -1:
                return 'YOU'
            else:
                return 'ENV'

    def step(self, action_X):
        self.state = copy.deepcopy(self.state)

        # Illegal move -- too high stack of squares
        if not np.all(self.state[0][action_X][5] == ConnectFourEnvironment.EMPTY):
            self.terminated = True
            if self.play_level in [-1, -2]:
                print(self.who_is_now() + " LOST ILLEGAL MOVE!")
                print(self.display())
            return self.ILLEGAL_MOVE_PENALTY

        self.apply_move(ConnectFourEnvironment.X, action_X)

        # Did X Win
        if self.check_winner(ConnectFourEnvironment.X, action_X):
            self.terminated = True
            if self.play_level in [-1, -2]:
                print(self.who_is_now() + " LOST!")
                print(self.display())
            return self.WIN_REWARD

        if self.game_over():
            self.terminated = True
            if self.play_level in [-1, -2]:
                print("A DRAW, " + self.who_is_now())
                print(self.display())
            return self.DRAW_REWARD

        if self.play_level in [-2, -3]:
            self.invert_state()
            if self.play_level == -2:
                print(self.display())
                input("Press key")
            return self.NOT_LOSS

        action_O = self.make_O_action()

        # Did O Win
        if self.check_winner(ConnectFourEnvironment.O, action_O):
            self.terminated = True
            if self.play_level in [-1, -2]:
                print(self.who_is_now() + " WON!")
                print(self.display())
            return self.LOSS_PENALTY

        if self.game_over():
            self.terminated = True
            return self.DRAW_REWARD

        return self.NOT_LOSS

    def invert_reward(self, r):
        if r == self.LOSS_PENALTY:
            return self.WIN_REWARD
        if r == self.WIN_REWARD:
            return self.LOSS_PENALTY
        return r

    def make_O_action(self):

        if self.play_level == -1:
            # manual mode
            print(self.display())
            action_O = int(input("Enter action (0..6)"))
            self.apply_move(ConnectFourEnvironment.O, action_O)
            return action_O

        free_columns = []
        for col in range(7):
            if np.all(self.state[0][col][5] == ConnectFourEnvironment.EMPTY):
                free_columns.append(col)

        if self.play_level > 0:
            # try to find winning move
            for action_O in free_columns:
                self.apply_move(ConnectFourEnvironment.O, action_O)
                if self.check_winner(ConnectFourEnvironment.O, action_O):
                    return action_O
                self.cancel_move(ConnectFourEnvironment.O, action_O)

        if self.play_level > 1:
            # prevent opponent making a connect four
            for action_T in free_columns:
                self.apply_move(ConnectFourEnvironment.X, action_T)
                prevent_win = self.check_winner(ConnectFourEnvironment.X, action_T)
                self.cancel_move(ConnectFourEnvironment.X, action_T)
                if prevent_win:
                    self.apply_move(ConnectFourEnvironment.O, action_T)
                    return action_T

        action_O = random.choice(free_columns)
        self.apply_move(ConnectFourEnvironment.O, action_O)
        return action_O

    def apply_move(self, player, action):
        for row in range(6):
            if np.all(self.state[0][action][row] == ConnectFourEnvironment.EMPTY):
                self.state[0][action][row] = player
                break

    def cancel_move(self, player, action):
        for row in range(6):
            # print('cancelling {}'.format(row))
            if np.all(self.state[0][action][5 - row] == player):
                self.state[0][action][5 - row] = ConnectFourEnvironment.EMPTY
                # print('canceled, col {} row {} '.format(action, 5 - row))
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

    def invert_state(self):
        self.reverted = not self.reverted
        if self.reverted:
            self.next_to_move = 1
        else:
            self.next_to_move = 0

        for row in range(6):
            for col in range(7):
                if np.all(self.state[0][col][row] == ConnectFourEnvironment.X):
                    self.state[0][col][row] = ConnectFourEnvironment.O
                elif np.all(self.state[0][col][row] == ConnectFourEnvironment.O):
                    self.state[0][col][row] = ConnectFourEnvironment.X

    def game_over(self):
        for col in range(7):
            if np.all(self.state[0][col][5] == ConnectFourEnvironment.EMPTY):
                return False
        return True

    def display(self):
        state = self.state[0]
        s = ""
        x = "X"
        o = "O"
        if self.reverted:
            x = "O"
            o = "X"

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
