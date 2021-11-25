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
assert(env.move_count == 7, "moves count")
assert(env.connect_four == Int8[], "connectfour")
assert(env.connect_four_count == 0, "connectfour count")

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
assert(env.move_count == 7, "moves count")
assert(env.connect_four == Int8[1,2,3,4], "connectfour")
assert(env.connect_four_count == 1, "connectfour count")

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

connectfour.move(env,3)
connectfour.move(env,4)

println(env)
assert(env.terminated == true, "terminated")
assert(env.illegal_action == false, "illegal_action")
assert(env.player == 1, "first player")
assert(env.reward == -1, "first player looses")
assert(env.move_count == 10, "moves count")
assert(env.connect_four == Int8[8,9,10,11], "connectfour")
assert(env.connect_four_count == 1, "connectfour count")

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
assert(env.move_count == 7, "moves count")
assert(env.connect_four == Int8[1,8,15,22], "connectfour")
assert(env.connect_four_count == 1, "connectfour count")

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
connectfour.move(env,7)

connectfour.move(env,4)

println(env)
assert(env.terminated == true, "terminated")
assert(env.illegal_action == false, "illegal_action")
assert(env.player == -1, "second player")
assert(env.reward == -1, "second player looses")
assert(env.move_count == 11, "moves count")
assert(env.connect_four == Int8[1,9,17,25], "connectfour")
assert(env.connect_four_count == 1, "connectfour count")

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
connectfour.move(env,1)

connectfour.move(env,4)

println(env)
assert(env.terminated == true, "terminated")
assert(env.illegal_action == false, "illegal_action")
assert(env.player == -1, "second player")
assert(env.reward == -1, "second player looses")
assert(env.move_count == 11, "moves count")
assert(env.connect_four == Int8[7,13,19,25], "connectfour")
assert(env.connect_four_count == 1, "connectfour count")