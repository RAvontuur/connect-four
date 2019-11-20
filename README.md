# connect-four


serverless version\
Monte-Carlo based (10.000 rollouts)

https://playboardgames.s3-eu-west-1.amazonaws.com/connectfour.html



## Documentation

**The environment (ConnectFourEnvironment / environment.py)**
* knows the current state of the play (position, termination, end-result, who-is-next)
* knows the rules of connect four
* knows how the state changes after an applied move

**The random player (Player_Random / player_random.py)**
* applies a random move [0..6] to the environment

**The Monte-Carlo player (Player_MonteCarlo / player_montecarlo.py)**
* starts a Monte-Carlo tree search
* choses the best move based on the statistics of the childs of the root of the analysis tree
* the root is the current state of the environment

**a node (MonteCarloTreeSearchNode / nodes.py)**
* is a node in an analysis tree
* contains the full state of a play (e.g. the position)
* contains the number of visits (back propagated for each roll-out towards the root node)
* contains the reward statistics (back propagated for each roll-out towards the root node)

a reward for a player is the same as a inverted reward for its opponent

**The Monte-Carlo tree search algorithm (MonteCarloTreeSearch / mcts/search.py)** 
* explores all children of the root node and executes one roll out 
* maintains an analysis tree, containing the statistics of the executed roll-outs
* back propagates the result of a roll out towards the root node for each parent node

a roll out is playing out a game from a certain position by making randomized moves 
(e.g. using the random player)

**The AWS Serverless Function (index.py)**
* start: restarts the environment to the initial position
* move(_action_): performs a move defined by _action_ on the environment 
* think: the Monte Carlo player will perform a move on the environment

**dynamo_repository.py**
* used for session management