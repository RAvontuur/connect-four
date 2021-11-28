#=
play:
- Julia version: 
- Author: ravontuur
- Date: 2021-11-24
=#

module ConnectFourEnvironmentTests

    using ConnectFour.ConnectFourEnvironment

    # test illegal move
    env = create_env()
    for i in range(1, length=7)
        move(env,4)
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
    env = create_env()
    move(env,1)
    move(env,1)
    move(env,2)
    move(env,2)
    move(env,3)
    move(env,3)
    move(env,4)

    println(env)
    @assert env.terminated == true
    @assert env.illegal_action == false
    @assert env.player == -1
    @assert env.reward == -1
    @assert env.move_count == 7
    @assert env.connect_four == Int8[1,2,3,4]
    @assert env.connect_four_count == 1

    # test horizontal 4 other player
    env = create_env()
    move(env,1)
    move(env,1)

    move(env,2)
    move(env,2)

    move(env,3)
    move(env,3)

    move(env,3)
    move(env,4)

    move(env,3)
    move(env,4)

    println(env)
    @assert env.terminated == true
    @assert env.illegal_action == false
    @assert env.player == 1
    @assert env.reward == -1
    @assert env.move_count == 10
    @assert env.connect_four == Int8[8,9,10,11]
    @assert env.connect_four_count == 1

    # test vertical 4
    env = create_env()
    move(env,1)
    move(env,2)

    move(env,1)
    move(env,2)

    move(env,1)
    move(env,2)

    move(env,1)

    println(env)
    @assert env.terminated == true
    @assert env.illegal_action == false
    @assert env.player == -1
    @assert env.reward == -1
    @assert env.move_count == 7
    @assert env.connect_four == Int8[1,8,15,22]
    @assert env.connect_four_count == 1

    # test diagonal 4
    env = create_env()
    move(env,1)
    move(env,2)

    move(env,2)
    move(env,3)

    move(env,3)
    move(env,4)

    move(env,3)
    move(env,4)

    move(env,4)
    move(env,7)

    move(env,4)

    println(env)
    @assert env.terminated == true
    @assert env.illegal_action == false
    @assert env.player == -1
    @assert env.reward == -1
    @assert env.move_count == 11
    @assert env.connect_four == Int8[1,9,17,25]
    @assert env.connect_four_count == 1

    # test diagonal 4  II
    env = create_env()
    move(env,7)
    move(env,6)

    move(env,6)
    move(env,5)

    move(env,5)
    move(env,4)

    move(env,5)
    move(env,4)

    move(env,4)
    move(env,1)

    move(env,4)

    println(env)
    @assert env.terminated == true
    @assert env.illegal_action == false
    @assert env.player == -1
    @assert env.reward == -1
    @assert env.move_count == 11
    @assert env.connect_four == Int8[7,13,19,25]
    @assert env.connect_four_count == 1

    # test draw, all occupied
    env = create_env()
    move(env,1);move(env,2);move(env,1);move(env,2);move(env,1);move(env,2);
    move(env,3);move(env,4);move(env,3);move(env,4);move(env,3);move(env,4);
    move(env,5);move(env,6);move(env,5);move(env,6);move(env,5);move(env,6);
    @assert env.move_count == 18
    @assert env.terminated == false
    move(env,7);move(env,1);move(env,7);move(env,1);move(env,7);move(env,1);
    move(env,2);move(env,3);move(env,2);move(env,3);move(env,2);move(env,3);
    move(env,4);move(env,5);move(env,4);move(env,5);move(env,4);move(env,5);
    @assert env.move_count == 36
    @assert env.terminated == false
    move(env,6);move(env,7);move(env,6);move(env,7);move(env,6);
    println(env)
    @assert env.move_count == 41
    @assert env.terminated == false

    move(env,7);
    println(env)
    @assert env.terminated == true
    @assert env.illegal_action == false
    @assert env.player == 1
    @assert env.reward == 0
    @assert env.move_count == 42
    @assert env.connect_four == Int8[]
    @assert env.connect_four_count == 0

    env = create_env()
    @assert env.move_count == 0
    @assert env.state[1,1] == 0
    copy = create_copy(env)
    @assert copy.move_count == 0
    @assert copy.state[1,1] == 0

    move(copy,1)
    # env should not change
    @assert env.move_count == 0
    @assert env.state[1,1] == 0
    # copy should change
    @assert copy.move_count == 1
    @assert copy.state[1,1] == 1


end