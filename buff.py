import numpy as np
import tensorflow as tf

# Generate a random numpy array of integers as input and corresponding output values
X_train = np.random.randint(0, 100, size=(100,), dtype=np.int32)  # Input array of integers
y_train = X_train * 2 + np.random.randint(0, 10, size=(100,), dtype=np.int32)  # Output array of integers

# Create a sequential model in TensorFlow
model = tf.keras.Sequential([
    tf.keras.layers.InputLayer(input_shape=(1,), dtype=tf.int32),  # Input layer with one input
    tf.keras.layers.Embedding(input_dim=100, output_dim=10),  # Embedding layer to represent integer inputs
    tf.keras.layers.Flatten(),  # Flatten the embedded input
    tf.keras.layers.Dense(1)  # Output layer with one output
])

# Compile the model
model.compile(optimizer='sgd', loss='mse')  # Using stochastic gradient descent optimizer and mean squared error loss

# Train the model
model.fit(X_train, y_train, epochs=100, batch_size=32)

# Generate a new numpy array of integers for prediction
X_test = np.array([50, 70, 90], dtype=np.int32)

# Predict using the trained model
y_pred = model.predict(X_test)

# Print the predicted values
print("Predicted values:")
for i in range(len(X_test)):
    print("Input: {}, Prediction: {}".format(X_test[i], y_pred[i][0]))
