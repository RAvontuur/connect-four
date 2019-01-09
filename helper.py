
def invert_reward(self, r):
    if r == self.LOSS_PENALTY:
        return self.WIN_REWARD
    if r == self.WIN_REWARD:
        return self.LOSS_PENALTY
    return r

    def invert_state(self):
        self.reverted = not self.reverted

        for row in range(6):
            for col in range(7):
                if np.all(self.state[0][col][row] == ConnectFourEnvironment.X):
                    self.state[0][col][row] = ConnectFourEnvironment.O
                elif np.all(self.state[0][col][row] == ConnectFourEnvironment.O):
                    self.state[0][col][row] = ConnectFourEnvironment.X