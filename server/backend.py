from flask import Flask, request, jsonify, send_file
import pandas as pd
import torch
from qiskit import Aer
from qiskit.utils import QuantumInstance
from qiskit_machine_learning.connectors import TorchConnector
from qiskit_machine_learning.neural_networks import TwoLayerQNN
from qiskit.circuit.library import RealAmplitudes
from qiskit.circuit import ParameterVector
import matplotlib.pyplot as plt
import io
import os
from flask_cors import CORS  # Enable CORS for all routes

import sys
sys.path.append('/Users/Tom/quantum/project/data')
from data import fetch_stock_data, preprocess_data

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Load the trained QNN model
def create_qnn(num_qubits):
    """Create a TwoLayerQNN with unique parameter names."""
    feature_map = RealAmplitudes(num_qubits, reps=1)
    feature_map_params = ParameterVector('fm_theta', feature_map.num_parameters)
    feature_map.assign_parameters(feature_map_params, inplace=True)

    ansatz = RealAmplitudes(num_qubits, reps=1)
    ansatz_params = ParameterVector('ansatz_theta', ansatz.num_parameters)
    ansatz.assign_parameters(ansatz_params, inplace=True)

    qnn = TwoLayerQNN(
        num_qubits=num_qubits,
        feature_map=feature_map,
        ansatz=ansatz,
        quantum_instance=QuantumInstance(Aer.get_backend("qasm_simulator"))
    )
    return qnn

qnn = create_qnn(num_qubits=4)
model = TorchConnector(qnn)
model = torch.nn.Sequential(model, torch.nn.Linear(1, 1))  # Add a linear layer

# Load the trained model parameters
MODEL_PATH = "../model/quantum_nn_model.pth"
if os.path.exists(MODEL_PATH):
    model.load_state_dict(torch.load(MODEL_PATH))
    print("Model loaded successfully.")
else:
    print("Model file not found. Ensure the model is trained and saved.")

# Utility function to create and save graphs as images
def create_graph(df, x_column, y_column, title):
    """Create a graph from the DataFrame and return it as a binary image."""
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.plot(df[x_column], df[y_column], marker='o', label=y_column)
    ax.set_title(title, fontsize=16)
    ax.set_xlabel(x_column, fontsize=14)
    ax.set_ylabel(y_column, fontsize=14)
    ax.legend(fontsize=12)
    ax.grid(True)

    # Save the plot to a BytesIO object
    image_io = io.BytesIO()
    plt.savefig(image_io, format='png', bbox_inches='tight')
    plt.close(fig)
    image_io.seek(0)  # Move the cursor to the beginning of the stream
    return image_io

# Route for predicting stock prices and returning an image
@app.route('/predict_image', methods=['POST'])
def predict_image():
    """Predict stock prices using the QNN model and return an image."""
    try:
        if 'file' not in request.files:
            return jsonify({"error": "No file uploaded."}), 400

        file = request.files['file']
        df = pd.read_csv(file)

        # Preprocess the input data
        features = ['open', 'high', 'low', 'close', 'volume', 'daily_return', '5_day_moving_avg', '30_day_moving_avg']
        X = df[features].values

        # Convert to PyTorch tensor
        X_torch = torch.tensor(X, dtype=torch.float32)

        # Make predictions
        predictions = model(X_torch).detach().numpy()
        df['predictions'] = predictions

        # Create the prediction graph
        graph_image = create_graph(df, x_column='index', y_column='predictions', title='Predicted Stock Prices')
        return send_file(graph_image, mimetype='image/png')
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Flask route for fetching stock data and returning an image
@app.route('/fetch_stock_image', methods=['GET'])
def fetch_stock_image():
    """Fetch stock data, preprocess it, and return an image."""
    try:
        ticker = request.args.get('ticker', default=None, type=str)
        if not ticker:
            return jsonify({"error": "Ticker symbol is required."}), 400

        # Fetch stock data
        df = fetch_stock_data(ticker)
        print(f"Data for {ticker} fetched successfully.")

        # Preprocess the stock data
        df_preprocessed = preprocess_data(df)
        print(f"Data preprocessing complete.")

        # Create the stock data graph
        graph_image = create_graph(df_preprocessed, x_column='index', y_column='close', title=f'{ticker} Stock Prices')
        return send_file(graph_image, mimetype='image/png')
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Flask route for default stock image
@app.route('/default_stock_image', methods=['GET'])
def default_stock_image():
    """Load default stock data and return an image."""
    try:
        # Load default stock data
        df = pd.read_csv('AAPL_preprocessed_data.csv')

        # Create the stock data graph
        graph_image = create_graph(df, x_column='index', y_column='close', title='Default Stock Prices (AAPL)')
        return send_file(graph_image, mimetype='image/png')
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Run the app
if __name__ == '__main__':
    app.run()
