import numpy as np
import random
import tensorflow as tf
import os
from vnetwork import Vnetwork

class TrainerValueNetwork():
    def __init__(self):

        # settings
        self.batch_size = 2000  # How many experiences to use for each training step.
        self.num_episodes = 1000  # How many episodes of game environment to train network with.
        self.periodically_save = 100
        self.load_model = False  # Whether to load a saved model.
        self.path = "./valuenetwork"  # The path to save our model to.


        #Make a path for our model to be saved in.
        if not os.path.exists(self.path):
            os.makedirs(self.path)

    def sample(self,nodes,size):
        return np.reshape(np.array(random.sample(nodes, size)),[size,2])


    def train(self, nodes):

        print("nodes size:" + str(len(nodes)))

        tf.reset_default_graph()
        mainQN = Vnetwork()

        init = tf.global_variables_initializer()

        saver = tf.train.Saver()

        with tf.Session() as sess:
            sess.run(init)
            if self.load_model:
                print('Loading Model...')
                ckpt = tf.train.get_checkpoint_state(self.path)
                saver.restore(sess,ckpt.model_checkpoint_path)

            for i in range(1, self.num_episodes+1):

                trainBatch = self.sample(nodes, self.batch_size)

                # update the network with our target values.
                _, loss = sess.run([mainQN.updateModel, mainQN.loss] ,
                     feed_dict={mainQN.scalarInput:np.vstack(trainBatch[:,0]),
                                mainQN.targetV:trainBatch[:,1]})

                print("loss: " + str(loss))

                #Periodically save the model.
                if i % self.periodically_save == 0:
                    file_name = 'model-{:d}-{:.3f}.ckpt'.format(i, loss)
                    saver.save(sess,self.path + '/' + file_name)
                    print("Saved Model " + file_name)

            print("FINISHED")
