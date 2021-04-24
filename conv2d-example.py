import numpy as np

import tensorflow as tf

# With `dilation_rate` as 2.
input_shape = (1, 7, 6, 2)
kernel1 = np.ones([7,6,2,5])

x = tf.random.normal(input_shape)
y = tf.keras.layers.Conv2D(
filters=5, kernel_size=(7,6), activation='relu',  input_shape=input_shape[1:],
  kernel_initializer=tf.constant_initializer(kernel1)
)(x)
print(y.shape)
print(x)
print(y)