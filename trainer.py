import numpy as np
import random
import tensorflow as tf
import os
from qnetwork import Qnetwork
from environment import ConnectFourEnvironment
from player_montecarlo import Player_MonteCarlo
from player_one_ahead import Player_One_Ahead
from player_neural import Player_Neural


# Experience Replay
# This class allows us to store experies and sample then randomly to train the network.
class experience_buffer():
    def __init__(self, buffer_size = 50000):
        self.buffer = []
        self.buffer_size = buffer_size

    def add(self,experience):
        if len(self.buffer) + len(experience) >= self.buffer_size:
            self.buffer[0:(len(experience)+len(self.buffer))-self.buffer_size] = []
        self.buffer.extend(experience)

    def sample(self,size):
        return np.reshape(np.array(random.sample(self.buffer,size)),[size,5])

# This is a simple function to resize our game frames.
def processState(states):
    return np.reshape(states,[7*6*2])

# These functions allow us to update the parameters of our target network with those of the primary network.
def updateTargetGraph(tfVars,tau):
    total_vars = len(tfVars)
    op_holder = []
    for idx,var in enumerate(tfVars[0:total_vars//2]):
        op_holder.append(tfVars[idx+total_vars//2].assign((var.value()*tau) + ((1-tau)*tfVars[idx+total_vars//2].value())))
    return op_holder

def updateTarget(op_holder,sess):
    for op in op_holder:
        sess.run(op)



class Trainer():
    def __init__(self):

        # settings
        self.opponent_training = None
        #self.opponent_training = Player_MonteCarlo(100)
        self.opponent_validation = Player_One_Ahead()
        self.batch_size = 32  # How many experiences to use for each training step.
        self.update_freq = 1  # How often to perform a training step.
        self.y = .99  # Discount factor on the target Q-values
        self.startE = 0.5  # Starting chance of random action
        self.endE = 0.01  # Final chance of random action
        self.greedy_moves = 3  # number of greedy initial moves
        self.greedy_moves_e = 0.5 # chance of random action during greedy initial moves
        self.annealing_episodes = 1000.  # How many steps of training to reduce startE to endE.
        self.num_episodes = 50000  # How many episodes of game environment to train network with.
        self.pre_train_episodes = 1000  # How many steps of random actions before training begins.
        self.max_epLength = 50  # The max allowed length of our episode.
        self.load_model = False  # Whether to load a saved model.
        self.path = "./dqn"  # The path to save our model to.
        self.tau = 0.001  # Rate to update target network toward primary network

        #Make a path for our model to be saved in.
        if not os.path.exists(self.path):
            os.makedirs(self.path)


    def train(self):

        tf.reset_default_graph()
        mainQN = Qnetwork()
        targetQN = Qnetwork()

        init = tf.global_variables_initializer()

        saver = tf.train.Saver()

        trainables = tf.trainable_variables()
        targetOps = updateTargetGraph(trainables, self.tau)

        myBuffer = experience_buffer()

        #Set the rate of random action decrease.
        e = self.startE

        #create lists to contain total rewards and steps per episode

        rList = []
        stepDrop = (self.startE - self.endE)/self.annealing_episodes

        with tf.Session() as sess:
            sess.run(init)
            if self.load_model:
                print('Loading Model...')
                ckpt = tf.train.get_checkpoint_state(self.path)
                saver.restore(sess,ckpt.model_checkpoint_path)

            player_in_training = Player_Neural(sess, mainQN)
            if self.opponent_training is None:
                self.opponent_training = player_in_training

            for i in range(1, self.num_episodes+1):
                pre_train = i < self.pre_train_episodes

                rGame, episodeBuffer = self.play_game(sess, mainQN,
                    e, pre_train and not self.load_model, self.greedy_moves, self.greedy_moves_e)
                rList.append(rGame)
                myBuffer.add(episodeBuffer.buffer)

                if not pre_train:
                    if e > self.endE:
                        e -= stepDrop

                    if i % (self.update_freq) == 0:
                        trainBatch = myBuffer.sample(self.batch_size) #Get a random batch of experiences.
                        #Below we perform the Double-DQN update to the target Q-values
                        Q1 = sess.run(mainQN.predict,feed_dict={mainQN.scalarInput:np.vstack(trainBatch[:,3])})
                        Q2 = sess.run(targetQN.Qout,feed_dict={targetQN.scalarInput:np.vstack(trainBatch[:,3])})
                        end_multiplier = -(trainBatch[:,4] - 1)
                        doubleQ = Q2[range(self.batch_size),Q1]
                        targetQ = trainBatch[:,2] + (self.y*doubleQ * end_multiplier)
                        #Update the network with our target values.
                        _ = sess.run(mainQN.updateModel,
                                     feed_dict={mainQN.scalarInput:np.vstack(trainBatch[:,0]),mainQN.targetQ:targetQ,
                                                mainQN.actions:trainBatch[:,1]})

                        updateTarget(targetOps,sess) #Update the target network toward the primary network.

                #Periodically save the model.
                if i % 1000 == 0:
                    rValidation = 0.0
                    for _ in range(100):
                        rGame = self.validate_play(player_in_training, self.opponent_validation)
                        rValidation += 0.5 + 0.5 * rGame
                    file_name = 'model-{:d}-{:.0f}.ckpt'.format(i, rValidation)
                    saver.save(sess,self.path + '/' + file_name)
                    print("Saved Model " + file_name)
                if i % 100 == 0:
                    print(i,np.mean(rList[-500:]), e)

            print("Percent of succesful episodes: {:.1f} %".format(50.0 + 50.0 * (sum(rList)/self.num_episodes)))

            return rList

    def play_game(self, sess, mainQN,  e, pre_train, greedy_moves, greedy_moves_e):

        episodeBuffer = experience_buffer()

        #Reset environment and get first new observation
        env = ConnectFourEnvironment()
        assert(env.next_to_move == 1)
        s = processState(env.state)
        r_game = 0
        j = 0
        #The Q-Network
        while j < self.max_epLength: #If the agent takes longer than 200 moves, end the trial.
            j+=1
            #Choose an action by greedily (with e chance of random action) from the Q-network
            e_mod = e
            if j <= greedy_moves:
                e_mod = greedy_moves_e
            if np.random.rand(1) < e_mod or pre_train:
                a = random.choice(env.get_legal_actions())
            else:
                a = sess.run(mainQN.predict,feed_dict={mainQN.scalarInput:[s]})[0]

            env = env.move(a)
            r = env.game_result(1)

            if not env.terminated:
                assert(env.next_to_move == -1)
                env = self.opponent_training.play(env)

            s1 = processState(env.state)
            d = env.terminated
            episodeBuffer.add(np.reshape(np.array([s,a,r,s1,d]),[1,5])) #Save the experience to our episode buffer.

            r_game += r
            s = s1

            if d:
                break

        return r_game, episodeBuffer

    def validate_play(self, player1, player2):
        env = ConnectFourEnvironment()

        while True:
            assert(env.next_to_move == 1)
            env = player1.play(env)
            if env.is_game_over():
                break

            assert(env.next_to_move == -1)
            env = player2.play(env)
            if env.is_game_over():
                break

        return env.game_result(1)