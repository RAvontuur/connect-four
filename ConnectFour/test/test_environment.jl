#=
play:
- Julia version: 
- Author: ravontuur
- Date: 2021-11-24
=#

import ConnectFour.ConnectFourEnvironment

# test illegal move
env = ConnectFourEnvironment.create_env()
for i in range(1, length=7)
    ConnectFourEnvironment.move(env,4)
end
println(env)
@assert env.terminated == true
@assert env.illegal_action == true
@assert env.player == -1
@assert env.reward == 1
@assert env.move_count == 7
@assert env.connect_four == Int8[]
@assert env.connect_four_count == 0

# test horizontal 4
env = ConnectFourEnvironment.create_env()
ConnectFourEnvironment.move(env,1)
ConnectFourEnvironment.move(env,1)
ConnectFourEnvironment.move(env,2)
ConnectFourEnvironment.move(env,2)
ConnectFourEnvironment.move(env,3)
ConnectFourEnvironment.move(env,3)
ConnectFourEnvironment.move(env,4)

println(env)
@assert env.terminated == true
@assert env.illegal_action == false
@assert env.player == -1
@assert env.reward == -1
@assert env.move_count == 7
@assert env.connect_four == Int8[1,2,3,4]
@assert env.connect_four_count == 1

# test horizontal 4 other player
env = ConnectFourEnvironment.create_env()
ConnectFourEnvironment.move(env,1)
ConnectFourEnvironment.move(env,1)

ConnectFourEnvironment.move(env,2)
ConnectFourEnvironment.move(env,2)

ConnectFourEnvironment.move(env,3)
ConnectFourEnvironment.move(env,3)

ConnectFourEnvironment.move(env,3)
ConnectFourEnvironment.move(env,4)

ConnectFourEnvironment.move(env,3)
ConnectFourEnvironment.move(env,4)

println(env)
@assert env.terminated == true
@assert env.illegal_action == false
@assert env.player == 1
@assert env.reward == -1
@assert env.move_count == 10
@assert env.connect_four == Int8[8,9,10,11]
@assert env.connect_four_count == 1

# test vertical 4
env = ConnectFourEnvironment.create_env()
ConnectFourEnvironment.move(env,1)
ConnectFourEnvironment.move(env,2)

ConnectFourEnvironment.move(env,1)
ConnectFourEnvironment.move(env,2)

ConnectFourEnvironment.move(env,1)
ConnectFourEnvironment.move(env,2)

ConnectFourEnvironment.move(env,1)

println(env)
@assert env.terminated == true
@assert env.illegal_action == false
@assert env.player == -1
@assert env.reward == -1
@assert env.move_count == 7
@assert env.connect_four == Int8[1,8,15,22]
@assert env.connect_four_count == 1

# test diagonal 4
env = ConnectFourEnvironment.create_env()
ConnectFourEnvironment.move(env,1)
ConnectFourEnvironment.move(env,2)

ConnectFourEnvironment.move(env,2)
ConnectFourEnvironment.move(env,3)

ConnectFourEnvironment.move(env,3)
ConnectFourEnvironment.move(env,4)

ConnectFourEnvironment.move(env,3)
ConnectFourEnvironment.move(env,4)

ConnectFourEnvironment.move(env,4)
ConnectFourEnvironment.move(env,7)

ConnectFourEnvironment.move(env,4)

println(env)
@assert env.terminated == true
@assert env.illegal_action == false
@assert env.player == -1
@assert env.reward == -1
@assert env.move_count == 11
@assert env.connect_four == Int8[1,9,17,25]
@assert env.connect_four_count == 1

# test diagonal 4  II
env = ConnectFourEnvironment.create_env()
ConnectFourEnvironment.move(env,7)
ConnectFourEnvironment.move(env,6)

ConnectFourEnvironment.move(env,6)
ConnectFourEnvironment.move(env,5)

ConnectFourEnvironment.move(env,5)
ConnectFourEnvironment.move(env,4)

ConnectFourEnvironment.move(env,5)
ConnectFourEnvironment.move(env,4)

ConnectFourEnvironment.move(env,4)
ConnectFourEnvironment.move(env,1)

ConnectFourEnvironment.move(env,4)

println(env)
@assert env.terminated == true
@assert env.illegal_action == false
@assert env.player == -1
@assert env.reward == -1
@assert env.move_count == 11
@assert env.connect_four == Int8[7,13,19,25]
@assert env.connect_four_count == 1