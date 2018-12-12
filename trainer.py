import numpy as np
import random
import tensorflow as tf
import tensorflow.contrib.slim as slim
import matplotlib.pyplot as plt
import scipy.misc
import os
from qnetwork import Qnetwork


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



def train(env):

    # settings
    batch_size = 32  # How many experiences to use for each training step.
    update_freq = 4  # How often to perform a training step.
    y = .99  # Discount factor on the target Q-values
    startE = 1  # Starting chance of random action
    endE = 0.1  # Final chance of random action
    annealing_steps = 10000.  # How many steps of training to reduce startE to endE.
    num_episodes = 10000  # How many episodes of game environment to train network with.
    pre_train_steps = 10000  # How many steps of random actions before training begins.
    max_epLength = 50  # The max allowed length of our episode.
    load_model = False  # Whether to load a saved model.
    path = "./dqn"  # The path to save our model to.
    tau = 0.001  # Rate to update target network toward primary network

    tf.reset_default_graph()
    mainQN = Qnetwork()
    targetQN = Qnetwork()

    init = tf.global_variables_initializer()

    saver = tf.train.Saver()

    trainables = tf.trainable_variables()

    targetOps = updateTargetGraph(trainables,tau)

    myBuffer = experience_buffer()

    #Set the rate of random action decrease.
    e = startE
    stepDrop = (startE - endE)/annealing_steps

    #create lists to contain total rewards and steps per episode
    jList = []
    rList = []
    total_steps = 0

    #Make a path for our model to be saved in.
    if not os.path.exists(path):
        os.makedirs(path)

    with tf.Session() as sess:
        sess.run(init)
        if load_model == True:
            print('Loading Model...')
            ckpt = tf.train.get_checkpoint_state(path)
            saver.restore(sess,ckpt.model_checkpoint_path)
        for i in range(num_episodes):
            episodeBuffer = experience_buffer()
            #Reset environment and get first new observation
            s = env.reset()
            s = processState(env.state)
            d = False
            rAll = 0
            j = 0
            #The Q-Network
            while j < max_epLength: #If the agent takes longer than 200 moves to reach either of the blocks, end the trial.
                j+=1
                #Choose an action by greedily (with e chance of random action) from the Q-network
                if np.random.rand(1) < e or total_steps < pre_train_steps:
                    a = np.random.randint(0,env.actions-1)
                else:
                    a = sess.run(mainQN.predict,feed_dict={mainQN.scalarInput:[s]})[0]
                r = env.step(a)
                s1 = processState(env.state)
                d = env.terminated
                total_steps += 1
                episodeBuffer.add(np.reshape(np.array([s,a,r,s1,d]),[1,5])) #Save the experience to our episode buffer.

                if total_steps > pre_train_steps:
                    if e > endE:
                        e -= stepDrop

                    if total_steps % (update_freq) == 0:
                        trainBatch = myBuffer.sample(batch_size) #Get a random batch of experiences.
                        #Below we perform the Double-DQN update to the target Q-values
                        Q1 = sess.run(mainQN.predict,feed_dict={mainQN.scalarInput:np.vstack(trainBatch[:,3])})
                        Q2 = sess.run(targetQN.Qout,feed_dict={targetQN.scalarInput:np.vstack(trainBatch[:,3])})
                        end_multiplier = -(trainBatch[:,4] - 1)
                        doubleQ = Q2[range(batch_size),Q1]
                        targetQ = trainBatch[:,2] + (y*doubleQ * end_multiplier)
                        #Update the network with our target values.
                        _ = sess.run(mainQN.updateModel, \
                                     feed_dict={mainQN.scalarInput:np.vstack(trainBatch[:,0]),mainQN.targetQ:targetQ, mainQN.actions:trainBatch[:,1]})

                        updateTarget(targetOps,sess) #Update the target network toward the primary network.
                rAll += r
                s = s1

                if d == True:

                    break

            myBuffer.add(episodeBuffer.buffer)
            jList.append(j)
            rList.append(rAll)
            #Periodically save the model.
            if i % 1000 == 0:
                saver.save(sess,path+'/model-'+str(i)+'.ckpt')
                print("Saved Model")
            if len(rList) % 10 == 0:
                print(total_steps,np.mean(rList[-10:]), e)
        saver.save(sess,path+'/model-'+str(i)+'.ckpt')
        print("Percent of succesful episodes: " + str(sum(rList)/num_episodes) + "%")

        return rList

