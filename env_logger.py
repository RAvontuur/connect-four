def str_action(f, action):
    for i in range(14):
        if i == action:
            f.write("1, ")
        else:
            f.write("0, ")

def str_valid_moves(f, moves, player):
    v = []
    for i in range(14):
        v.append(0)

    for move in moves:
        if player == 1:
            v[2*move] = 1
        else:
            v[2*move+1] = 1

    first = True
    for i in v:
        if not first:
            f.write(", ")
        f.write(str(i))
        first = False

class EnvLogger:

    LOG_BOARD_BEFORE_ACTION = 0
    LOG_ACTION = 1
    LOG_BOARD_AFTER_ACTION = 2
    LOG_CONNECT_FOUR_LABELS = 3
    LOG_VALID_MOVES_BEFORE = 4
    LOG_VALID_MOVES_AFTER = 5

    def __init__(self, file_name, settings = [LOG_BOARD_AFTER_ACTION, LOG_CONNECT_FOUR_LABELS]):
        self.f = open(file_name,"w+")
        self.settings = settings

    def close(self):
        self.f.close

    def log_before_action(self, env, action):
        if EnvLogger.LOG_BOARD_BEFORE_ACTION in self.settings:
            self.f.write(env.display_csv())
            self.f.write(", ")

        if EnvLogger.LOG_VALID_MOVES_BEFORE in self.settings:
            str_valid_moves(self.f, env.get_legal_actions(), env.get_player())

        if EnvLogger.LOG_ACTION in self.settings:
            if env.get_player() == 1:
                str_action(self.f, 2 * action)
            else:
                str_action(self.f, 2 * action + 1)

    def log(self, env):
        if EnvLogger.LOG_BOARD_AFTER_ACTION in self.settings:
            self.f.write(env.display_csv())
            if EnvLogger.LOG_CONNECT_FOUR_LABELS in self.settings:
                self.f.write(", ")

        if EnvLogger.LOG_CONNECT_FOUR_LABELS in self.settings:
            if env.game_result(1) == 1:
                self.f.write(str(env.connect_four_count) + ", ")
            else:
                self.f.write("0, ")

            if env.game_result(-1) == 1:
                self.f.write(str(env.connect_four_count))
            else:
                self.f.write("0")
            if EnvLogger.LOG_VALID_MOVES_AFTER in self.settings:
                self.f.write(", ")

        if EnvLogger.LOG_VALID_MOVES_AFTER in self.settings:
            str_valid_moves(self.f, env.get_legal_actions(), env.get_player())

        self.f.write("\n")
