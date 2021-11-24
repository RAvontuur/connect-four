#=
play:
- Julia version: 
- Author: ravontuur
- Date: 2021-11-24
=#


    ILLEGAL_MOVE_PENALTY = -1
    NOT_LOSS = 0

    mutable struct ConnectFourEnvironment
        player
        state
        last_action
        reward
        terminated
        illegal_action
        move_count
    end

    function create_env()
        return ConnectFourEnvironment(1, zeros(Int8, 7, 6), 0, 0, false, false, 0)
    end

    function finish(self, result, terminate = false, illegal = false)
        println("finish")
        self.illegal_action = illegal
        self.terminated = terminate
        self.player = -self.player
        self.reward = -result
        self.move_count += 1
        return self
    end

    function apply_move(self, action)
        for row in range(1, length=6)
            if self.state[action, row] == 0
                self.state[action, row] = self.player
                return self
            end
        end
    end

    function move(self, action)
        self.last_action = action
        if self.state[action, 6] != 0
            return finish(self, ILLEGAL_MOVE_PENALTY, true, true)
        end

        self = apply_move(self, action)
        return finish(self, NOT_LOSS)
    end


    function assert(b, s)
        if b == false
           throw(InvalidStateException("assertion failed", Symbol(s)))
        end
    end

# test illegal move
env = create_env()
for row in range(1, length=7)
    move(env,4)
    println(env)
end
assert(env.terminated == true, "terminated")
assert(env.illegal_action == true, "illegal_action")

