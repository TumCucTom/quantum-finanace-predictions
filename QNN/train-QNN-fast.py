import numpy as np
import pandas as pd
from qiskit import Aer
from qiskit.circuit.library import RealAmplitudes
from qiskit.utils import QuantumInstance
from qiskit_machine_learning.neural_networks import TwoLayerQNN
from qiskit_machine_learning.connectors import TorchConnector
from qiskit.circuit import ParameterVector
from sklearn.model_selection import train_test_split
from sklearn.utils import shuffle
import torch
from torch import nn
from sklearn.preprocessing import MinMaxScaler
import matplotlib.pyplot as plt
import pickle
import time

# Example function to prepare and split the data
def prepare_data(df, features, target, test_size=0.2, num_samples=100):
    """Prepare and split the data into training and testing sets, and reduce dataset size."""
    X = df[features].values
    y = df[target].values
    X, y = shuffle(X, y, random_state=42)
    X, y = X[:num_samples], y[:num_samples]  # Reduce dataset size
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=test_size, random_state=42)
    return X_train, X_test, y_train, y_test

# Create a quantum neural network
def create_qnn(num_qubits):
    """Create a TwoLayerQNN with unique parameter names and a shallow circuit."""
    # Feature map
    feature_map = RealAmplitudes(num_qubits, reps=1)  # Shallow circuit
    feature_map_params = ParameterVector('fm_theta', feature_map.num_parameters)
    feature_map.assign_parameters(feature_map_params, inplace=True)

    # Ansatz
    ansatz = RealAmplitudes(num_qubits, reps=1)  # Shallow circuit
    ansatz_params = ParameterVector('ansatz_theta', ansatz.num_parameters)
    ansatz.assign_parameters(ansatz_params, inplace=True)

    # TwoLayerQNN
    qnn = TwoLayerQNN(
        num_qubits=num_qubits,
        feature_map=feature_map,
        ansatz=ansatz,
        quantum_instance=QuantumInstance(
            Aer.get_backend("qasm_simulator"),
            shots=1024,
            optimization_level=1,
            backend_options={"max_parallel_threads": 4}  # Enable parallelization
        )
    )
    return qnn

# Training the QNN with PyTorch
def train_qnn(X_train, y_train, num_qubits=4, epochs=10, learning_rate=0.01):
    """Train a quantum neural network using PyTorch."""
    qnn = create_qnn(num_qubits)

    # Connect QNN to PyTorch
    model = TorchConnector(qnn)
    model = nn.Sequential(model, nn.Linear(1, 1))  # Add a linear layer

    # Define loss function and optimizer
    loss_function = nn.MSELoss()
    optimizer = torch.optim.Adam(model.parameters(), lr=learning_rate)

    # Convert data to PyTorch tensors
    X_train_torch = torch.tensor(X_train, dtype=torch.float32)
    y_train_torch = torch.tensor(y_train, dtype=torch.float32)

    # Training loop
    losses = []
    start_time = time.time()
    for epoch in range(epochs):
        optimizer.zero_grad()
        predictions = model(X_train_torch)
        loss = loss_function(predictions.flatten(), y_train_torch)
        loss.backward()
        optimizer.step()

        losses.append(loss.item())
        print(f"Epoch {epoch + 1}/{epochs}, Loss: {loss.item()}")

    end_time = time.time()
    print(f"Training completed in {end_time - start_time:.2f} seconds")
    return model, losses

# Save the trained QNN model
def save_qnn_model(model, filename="quantum_nn_model.pth"):
    """Save the trained quantum neural network model to a file."""
    torch.save(model.state_dict(), filename)
    print(f"Model saved as {filename}")

# Load the saved model
def load_qnn_model(qnn, filename="quantum_nn_model.pth"):
    """Load the saved quantum neural network model from a file."""
    model = TorchConnector(qnn)
    model.load_state_dict(torch.load(filename))
    return model

# Visualize the loss during training
def plot_loss(losses):
    """Plot the loss during the training process."""
    plt.plot(losses)
    plt.title("Quantum Neural Network Training Loss")
    plt.xlabel("Epochs")
    plt.ylabel("Loss (MSE)")
    plt.show()

# Example usage
if __name__ == '__main__':
    # Load the preprocessed data (replace this with your preprocessed data)
    df = pd.read_csv('../data/AAPL_preprocessed_data.csv')

    # Prepare the data: Features (columns) and target (column to predict)
    features = ['open', 'high', 'low', 'close', 'volume', 'daily_return', '5_day_moving_avg', '30_day_moving_avg']
    target = 'close'  # Target is the closing price
    X_train, X_test, y_train, y_test = prepare_data(df, features, target, num_samples=100)

    # Train the QNN
    model, losses = train_qnn(X_train, y_train, num_qubits=4, epochs=10, learning_rate=0.01)

    # Save the trained QNN model
    save_qnn_model(model, "../model/quantum_nn_model.pth")

    # Plot the training loss
    plot_loss(losses)
