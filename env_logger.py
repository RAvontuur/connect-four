class EnvLogger:

    def __init__(self, file_name):
        self.f = open(file_name,"w+")

    def close(self):
        self.f.close

    def log(self, env):
        if env.game_result(1) == 1:
            self.f.write("1, ")
        else:
            self.f.write("0, ")

        if env.game_result(-1) == 1:
            self.f.write("1")
        else:
            self.f.write("0")

        self.f.write(env.display_csv())
        self.f.write("\n")