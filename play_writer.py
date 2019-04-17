
class PlayWriter:

    def __init__(self, file_name, write=False):
        self.f = open("mcts.txt","w+")

    def close(self):
        self.f.close

    def write_play(self, env, value, visits):
        self.f.write(env.get_game_state_short())
        self.f.write(",")
        self.f.write(str(value))
        self.f.write(",")
        self.f.write(str(visits))
        self.f.write("\n")


