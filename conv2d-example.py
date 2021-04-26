import numpy as np

import tensorflow as tf

input_shape = (1, 7, 6, 2)
kernel1 = np.zeros([4,4,2,2])
# kernel1[0,0,0,0] = 1

# horizontal
kernel1[1,0,0,0] = 1
kernel1[1,1,0,0] = 1
kernel1[1,2,0,0] = 1
kernel1[1,3,0,0] = 1

# vertical
kernel1[0,1,0,1] = 1
kernel1[1,1,0,1] = 1
kernel1[2,1,0,1] = 1
kernel1[3,1,0,1] = 1

x = np.zeros(input_shape)
# x[0,0,0,0] = 1
# x[0,1,0,0] = 1
# x[0,2,0,0] = 1
# x[0,3,0,0] = 1
# x[0,4,0,0] = 1
# x[0,5,0,0] = 1
# x[0,6,0,0] = 1
# x[0,0,0,0] = 1
# x[0,0,1,0] = 1
# x[0,0,2,0] = 1
# x[0,0,3,0] = 1
# x[0,0,4,0] = 1
# x[0,1,1,0] = 1
x[0,6,2,0] = 1
x[0,6,3,0] = 1
x[0,6,4,0] = 1
x[0,6,5,0] = 1
# x[0,1,6,0] = 1


y = tf.keras.layers.Conv2D(
  filters=2, kernel_size=(4,4),
  padding='same',
  input_shape=input_shape[1:],
  kernel_initializer=tf.constant_initializer(kernel1)
)(x)
print(y.shape)
print(x)
print(y)