def str_action(f, action):
    for i in range(14):
        if i == action:
            f.write("1, ")
        else:
            f.write("0, ")

class EnvLogger:

    LOG_BOARD_BEFORE_ACTION = 0
    LOG_ACTION = 1
    LOG_BOARD_AFTER_ACTION = 2
    LOG_CONNECT_FOUR_LABELS = 3

    def __init__(self, file_name, settings = [LOG_BOARD_AFTER_ACTION, LOG_CONNECT_FOUR_LABELS]):
        self.f = open(file_name,"w+")
        self.settings = settings

    def close(self):
        self.f.close

    def log_before_action(self, env, action):
        if EnvLogger.LOG_BOARD_BEFORE_ACTION in self.settings:
            self.f.write(env.display_csv())
            self.f.write(", ")
        if EnvLogger.LOG_ACTION:
            if env.next_to_move == 1:
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

        self.f.write("\n")
