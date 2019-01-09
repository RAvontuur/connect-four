class Player_Manual:

    def __init__(self,  player):
        self.player = player

    def play(self, env):
        assert(env.next_to_move == self.player)
        assert(env.terminated == False)

        print(env)
        action = int(input("Enter action (0..6)"))

        return env.move(action)