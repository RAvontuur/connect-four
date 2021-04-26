from tensorflow.python.keras import backend
from tensorflow.python.keras.layers.pooling import GlobalPooling2D


class GlobalSumPooling2D(GlobalPooling2D):
  """Global sum pooling operation for spatial data.

  Examples:

  >>> input_shape = (2, 4, 5, 3)
  >>> x = tf.random.normal(input_shape)
  >>> y = tf.keras.layers.GlobalSumPooling2D()(x)
  >>> print(y.shape)
  (2, 3)

  Arguments:
      data_format: A string,
        one of `channels_last` (default) or `channels_first`.
        The ordering of the dimensions in the inputs.
        `channels_last` corresponds to inputs with shape
        `(batch, height, width, channels)` while `channels_first`
        corresponds to inputs with shape
        `(batch, channels, height, width)`.
        It defaults to the `image_data_format` value found in your
        Keras config file at `~/.keras/keras.json`.
        If you never set it, then it will be "channels_last".

  Input shape:
    - If `data_format='channels_last'`:
      4D tensor with shape `(batch_size, rows, cols, channels)`.
    - If `data_format='channels_first'`:
      4D tensor with shape `(batch_size, channels, rows, cols)`.

  Output shape:
    2D tensor with shape `(batch_size, channels)`.
  """

  def call(self, inputs):
    if self.data_format == 'channels_last':
      return backend.sum(inputs, axis=[1, 2])
    else:
      return backend.sum(inputs, axis=[2, 3])