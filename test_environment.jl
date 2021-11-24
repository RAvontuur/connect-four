#=
play:
- Julia version: 
- Author: ravontuur
- Date: 2021-11-24
=#

include("connectfour.jl")

    function assert(b, s)
        if b == false
           throw(InvalidStateException("assertion failed", Symbol(s)))
        end
    end

# test illegal move
env = connectfour.create_env()
for i in range(1, length=7)
    connectfour.move(env,4)
end
println(env)
assert(env.terminated == true, "terminated")
assert(env.illegal_action == true, "illegal_action")
assert(env.player == -1, "second player")
assert(env.reward == 1, "second player wins")

# test horizontal 4
env = connectfour.create_env()
connectfour.move(env,1)
connectfour.move(env,1)
connectfour.move(env,2)
connectfour.move(env,2)
connectfour.move(env,3)
connectfour.move(env,3)
connectfour.move(env,4)

println(env)
assert(env.terminated == true, "terminated")
assert(env.illegal_action == false, "illegal_action")
assert(env.player == -1, "second player")
assert(env.reward == -1, "second player looses")

# test horizontal 4 other player
env = connectfour.create_env()
connectfour.move(env,1)
connectfour.move(env,1)
connectfour.move(env,2)
connectfour.move(env,2)
connectfour.move(env,3)
connectfour.move(env,3)
connectfour.move(env,3)
connectfour.move(env,4)

println(env)
assert(env.terminated == true, "terminated")
assert(env.illegal_action == false, "illegal_action")
assert(env.player == 1, "first player")
assert(env.reward == -1, "first player looses")

# test vertical 4
env = connectfour.create_env()
connectfour.move(env,1)
connectfour.move(env,2)
connectfour.move(env,1)
connectfour.move(env,2)
connectfour.move(env,1)
connectfour.move(env,2)
connectfour.move(env,1)

println(env)
assert(env.terminated == true, "terminated")
assert(env.illegal_action == false, "illegal_action")
assert(env.player == -1, "second player")
assert(env.reward == -1, "second player looses")

# test diagonal 4
env = connectfour.create_env()
connectfour.move(env,1)
connectfour.move(env,2)

connectfour.move(env,2)
connectfour.move(env,3)

connectfour.move(env,3)
connectfour.move(env,4)

connectfour.move(env,3)
connectfour.move(env,4)

connectfour.move(env,4)
connectfour.move(env,5)

connectfour.move(env,4)

println(env)
assert(env.terminated == true, "terminated")
assert(env.illegal_action == false, "illegal_action")
assert(env.player == -1, "second player")
assert(env.reward == -1, "second player looses")

# test diagonal 4  II
env = connectfour.create_env()
connectfour.move(env,7)
connectfour.move(env,6)

connectfour.move(env,6)
connectfour.move(env,5)

connectfour.move(env,5)
connectfour.move(env,4)

connectfour.move(env,5)
connectfour.move(env,4)

connectfour.move(env,4)
connectfour.move(env,3)

connectfour.move(env,4)

println(env)
assert(env.terminated == true, "terminated")
assert(env.illegal_action == false, "illegal_action")
assert(env.player == -1, "second player")
assert(env.reward == -1, "second player looses")