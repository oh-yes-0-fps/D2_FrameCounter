import numpy as np
import tensorflow as tf
import json
import os
FILE_NAME = "data/aa_frame_data_harm_combined.json"
TRAIN = 'aa'
DIRECTION = 'horizontal'

with open(FILE_NAME, "r") as f:
    jdata: dict[str, dict] = json.load(f)

lst = list(jdata.keys())
#sort by string as int
lst.sort(key=lambda x: int(x))

aa_x = []
pixels = []
for aa in lst:
    buffer = []
    for x in jdata[aa]["data"][DIRECTION]:
        buffer.append(x[0])
    pixels.append(buffer)
    aa_x.append(int(aa))

X_train = np.array(pixels)
# Generate a random numpy array and target value for training
y_train = np.array(aa_x)  # Target value

checkpoint_path = "checkpoints/cp.ckpt"
checkpoint_dir = os.path.dirname(checkpoint_path)

cp_callback = tf.keras.callbacks.ModelCheckpoint(filepath=checkpoint_path,
                                                 save_weights_only=True,
                                                 verbose=1)


# Create a sequential model in TensorFlow
model = tf.keras.Sequential([
    tf.keras.layers.InputLayer(input_shape=(192,), dtype=tf.float32),  # Input layer with shape (192,)
    tf.keras.layers.Dense(256, activation='relu'),  # Hidden layer with 256 neurons and ReLU activation
    tf.keras.layers.Dense(128, activation='relu'),  # Hidden layer with 128 neurons and ReLU activation
    tf.keras.layers.Dense(64, activation='relu'),  # Hidden layer with 64 neurons and ReLU activation
    tf.keras.layers.Dense(1)  # Output layer with one output
])

latest = tf.train.latest_checkpoint(checkpoint_dir)

model.load_weights(latest)

# Compile the model
model.compile(optimizer='Adagrad', loss='mae')  # Using stochastic gradient descent optimizer and mean squared error loss

# Train the model
model.fit(X_train, y_train, epochs=1000, batch_size=1, callbacks=[cp_callback])

model.save('models/ar_'+TRAIN)

