import numpy as np
import tensorflow as tf

class DoubleQLearner():

    def __init__(self, mainQN, targetQN):
        self.gamma = .99  # Discount factor on the target Q-values
        self.tau = 1.0  # Rate to update target network toward primary network

        self.mainQN = mainQN
        self.targetQN = targetQN

        self.trainables = tf.trainable_variables()
        self.targetOps = self.updateTargetGraph(self.trainables, self.tau)


    def learn(self, sess, trainBatch):
        # below we perform the Double-DQN update to the target Q-values
        # experience format trainBatch: [[s,a,r,s1,d], ..]

        # calculate the actions for each experienced state, the state after applying the chosen action
        # using the main neural network (the results for the terminated plays will not be used)
        A1 = sess.run(self.mainQN.predict,feed_dict={self.mainQN.scalarInput:np.vstack(trainBatch[:,3])})

        # calculate the Q's for each experienced state, the state after applying the chosen action
        # using the target neural network  (the results for the terminated plays will not be used)
        Q2 = sess.run(self.mainQN.Qout,feed_dict={self.mainQN.scalarInput:np.vstack(trainBatch[:,3])})

        # retrieve the value for the calculated best action, based on the double neural networks
        # this is a best estimate, based on learning from experiences
        doubleV = Q2[range(len(trainBatch)),A1]

        # True = 1,  False = 0
        not_terminated = 1 - trainBatch[:,4]

        # ignore terminated doubleV's
        # for terminated plays use the rewards directly
        targetQ = trainBatch[:,2] + (self.gamma * doubleV * not_terminated)

        # update the network with our target values.
        _ = sess.run(self.mainQN.updateModel,
                     feed_dict={self.mainQN.scalarInput:np.vstack(trainBatch[:,0]),
                                self.mainQN.targetQ:targetQ,
                                self.mainQN.actions:trainBatch[:,1]})

        # partly update the target network toward the primary network.
        self.updateTarget(self.targetOps, sess)



    #----------------------------------------
    # These functions allow us to update the parameters of our target network with those of the primary network.
    def updateTargetGraph(self, tfVars, tau):
        total_vars = len(tfVars)
        print("total_vars: " + str(total_vars))
        op_holder = []
        for idx,var in enumerate(tfVars[0:total_vars//2]):
            print("idx: " + str(idx) + " var: " + str(var) + " target: " + str(tfVars[idx+total_vars//2]))
            op_holder.append(tfVars[idx+total_vars//2].assign((var.value()*tau) + ((1-tau)*tfVars[idx+total_vars//2].value())))
        return op_holder

    def updateTarget(self, op_holder, sess):
        for op in op_holder:
            sess.run(op)