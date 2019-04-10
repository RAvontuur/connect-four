import tensorflow as tf
import tensorflow.contrib.slim as slim

class Vnetwork():
  def __init__(self):
    h_size = 7*14  # The size of the final convolutional layer

    # The network recieves a frame from the game, flattened into an array.
    # It then resizes it and processes it through four convolutional layers.
    self.scalarInput = tf.placeholder(shape=[None, 7 * 6 * 2], dtype=tf.float32)
    self.imageIn = tf.reshape(self.scalarInput, shape=[-1, 7, 6, 2])
    self.conv1 = slim.conv2d( \
        inputs=self.imageIn, num_outputs=32, kernel_size=[4, 4], stride=[1, 1], padding='SAME',
        biases_initializer=None)
    self.conv2 = slim.conv2d( \
        inputs=self.conv1, num_outputs=64, kernel_size=[3, 3], stride=[1, 1], padding='SAME', biases_initializer=None)
    self.conv3 = slim.conv2d( \
        inputs=self.conv2, num_outputs=64, kernel_size=[2, 2], stride=[1, 1], padding='SAME', biases_initializer=None)
    self.conv4 = slim.conv2d( \
        inputs=self.conv3, num_outputs=h_size, kernel_size=[7, 6], stride=[1, 1], padding='VALID',
        biases_initializer=None)

    self.streamV = slim.flatten(self.conv4)
    xavier_init = tf.contrib.layers.xavier_initializer()
    self.VW = tf.Variable(xavier_init([h_size, 1]))
    self.V = tf.matmul(self.streamV, self.VW)

    # Below we obtain the loss by taking the sum of squares difference between the target and prediction V values.
    self.targetV = tf.placeholder(shape=[None], dtype=tf.float32)

    self.td_error = tf.square(self.targetV - self.V)
    self.loss = tf.reduce_mean(self.td_error)
    self.trainer = tf.train.AdamOptimizer(learning_rate=0.0001)
    self.updateModel = self.trainer.minimize(self.loss)
