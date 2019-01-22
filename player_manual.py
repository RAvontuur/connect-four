class Player_Manual:

    def play(self, env):
        assert(env.terminated == False)

        print(env)
        action = int(input("Enter action (0..6)"))

        return env.move(action)