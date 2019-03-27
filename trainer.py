import numpy as np
import random
import tensorflow as tf
import os
import player_neural
from qnetwork import Qnetwork
from double_q_learner import DoubleQLearner
from environment import ConnectFourEnvironment
from player_montecarlo import Player_MonteCarlo
from player_one_ahead import Player_One_Ahead
from player_neural import Player_Neural
from player_random import Player_Random


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

def create_opponent_training(sess, mainQN):
    player_rollout = Player_Neural(sess, mainQN)
    return Player_MonteCarlo(7, rollout_player=player_rollout)


class Trainer():
    def __init__(self):

        # settings
        # self.opponent_training = None
        # self.opponent_training = Player_One_Ahead()
        self.opponent_training = None
        self.opponent_validation = Player_MonteCarlo(7, rollout_player=Player_One_Ahead())
        self.batch_size = 32  # How many experiences to use for each training step.
        self.update_freq = 1  # How often to perform a training step.
        self.startE = 0.5  # Starting chance of random action
        self.endE = 0.01  # Final chance of random action
        self.annealing_episodes = 1000.  # How many steps of training to reduce startE to endE.
        self.num_episodes = 200000  # How many episodes of game environment to train network with.
        self.pre_train_episodes = 1000  # How many steps of random actions before training begins.
        self.max_epLength = 50  # The max allowed length of our episode.
        self.periodically_save = 1000
        self.load_model = False  # Whether to load a saved model.
        self.path = "./dqn"  # The path to save our model to.


        #Make a path for our model to be saved in.
        if not os.path.exists(self.path):
            os.makedirs(self.path)


    def train(self):

        tf.reset_default_graph()
        mainQN = Qnetwork()
        targetQN = Qnetwork()

        init = tf.global_variables_initializer()

        saver = tf.train.Saver()

        myBuffer = experience_buffer()

        learner = DoubleQLearner(mainQN, targetQN)

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
            player_target = Player_Neural(sess, targetQN)
            player_pre_train = Player_Random()
            if self.opponent_training is None:
                self.opponent_training = create_opponent_training(sess, mainQN)

            for i in range(1, self.num_episodes+1):
                pre_train = i < self.pre_train_episodes

                if pre_train:
                    player = player_pre_train
                else:
                    player = player_in_training

                rGame, episodeBuffer = self.play_game(player, self.opponent_training)
                rList.append(rGame)
                myBuffer.add(episodeBuffer.buffer)

                if not pre_train:
                    if e > self.endE:
                        e -= stepDrop

                    if i % (self.update_freq) == 0:
                        #Get a random batch of experiences.
                        trainBatch = myBuffer.sample(self.batch_size)
                        assert(len(trainBatch) == self.batch_size)
                        learner.learn(sess, trainBatch)

                #Periodically save the model.
                if i % self.periodically_save == 0:
                    rValidation = 0.0
                    for _ in range(100):
                        rGame, _ = self.play_game(player_in_training, self.opponent_validation)
                        rValidation += 0.5 + 0.5 * float(rGame)
                    rValidation2 = 0.0
                    for _ in range(100):
                        rGame, _ = self.play_game(player_target, self.opponent_validation)
                        rValidation2 += 0.5 + 0.5 * float(rGame)
                    rValidation3 = 0.0
                    for _ in range(100):
                        rGame, _ = self.play_game(player_in_training, self.opponent_training)
                        rValidation3 += 0.5 + 0.5 * float(rGame)
                    print("main: " + str(rValidation) + " target: " + str(rValidation2) + " opponent: " + str(rValidation3))
                    file_name = 'model-{:d}-{:.0f}.ckpt'.format(i, rValidation)
                    saver.save(sess,self.path + '/' + file_name)
                    print("Saved Model " + file_name)

                    # upgrade the opponent
                    self.opponent_training = create_opponent_training(sess, mainQN)
                if i % 100 == 0:
                    print(i,np.mean(rList[-500:]), e)

            print("FINISHED")

    def play_game(self, player_pupil, player_master):

        episodeBuffer = experience_buffer()

        #Reset environment and get first new observation
        env = ConnectFourEnvironment()
        assert(env.next_to_move == 1)
        s = player_neural.processState(env)
        while True:
            env, a = player_pupil.play(env)
            r = env.game_result(1)

            if not env.terminated:
                assert(env.next_to_move == -1)
                env, a1 = player_master.play(env)

            s1 = player_neural.processState(env)
            d = env.terminated
            episodeBuffer.add(np.reshape(np.array([s,a,r,s1,d]),[1,5])) #Save the experience to our episode buffer.

            s = s1

            if env.terminated:
                break

        return env.game_result(1), episodeBuffer