# connect-four




run 1\
/ oneahead / mainQN = targetQN \
50.000 35

run2 \
oneahead / mainQN = targetQN\
10.000 22.8\
20.000 27.0\
30.000 31.9\
40.000  38.8\
50.000 39.9\
70.000 45.1\
100.00 51.5\
120.000 55.7\
150.000 62.3\
200.000 61.3

run3 \
oneahead / mainQN = targetQN\
10.000 15.2\
20.000 24.6\
30.000 32.4\
40.000 34.6\
50.000 37.9\
60.000 39.8

Monte Carlo, using a payer for roll-out:

player1 = Player_Neural()\
player_rollout = Player_One_Ahead(2)\
player2 = Player_MonteCarlo(1000, rollout_player=player_rollout)\
20-10 (slow)\
4-6 (avg 147 sec per play)\
6-4 (avg 68 sec, after refactoring player_one_ahead)

player1 = Player_Neural()\
player2 = Player_One_Ahead(2)\
63-37\
37-63 (avg 14 ms, after refactoring player_one_ahead)

player1 = Player_Neural()\
player2 = Player_MonteCarlo(1000, rollout_player=None)\
26-14

player1 = Player_Neural()\
player2 = Player_Random()\
38-2

Monte Carlo performance optimalisatie:
player1 = Player_One_Ahead(2)\
player_rollout = Player_One_Ahead(2)\
player2 = Player_MonteCarlo(1000, rollout_player=player_rollout)\
10-0 : 62 sec per play (using own deepcopy implementation)

