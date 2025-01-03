from flask import Flask, request, jsonify
import pandas as pd
import torch
from qiskit import Aer
from qiskit.utils import QuantumInstance
from qiskit_machine_learning.connectors import TorchConnector
from qiskit_machine_learning.neural_networks import TwoLayerQNN
from qiskit.circuit.library import RealAmplitudes
from qiskit.circuit import ParameterVector
import yfinance as yf
import os
from flask_cors import CORS  # Import CORS

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

# Route for predicting stock prices
@app.route('/predict', methods=['POST'])
def predict():
    """Predict stock prices using the QNN model."""
    print('predicting')
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

        return df.to_json(orient='records')
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Flask route for fetching stock data
@app.route('/fetch_stock', methods=['GET'])
def fetch_stock():
    """Fetch stock data from Alpha Vantage and preprocess it."""
    try:
        ticker = request.args.get('ticker', default=None, type=str)
        if not ticker:
            return jsonify({"error": "Ticker symbol is required."}), 400

        # Fetch stock data from Alpha Vantage
        df = fetch_stock_data(ticker)
        print(f"Data for {ticker} fetched successfully.")

        # Preprocess the stock data
        df_preprocessed = preprocess_data(df)
        print(f"Data preprocessing complete.")

        # Convert the preprocessed data to JSON and return it
        return df_preprocessed.to_json(orient='records')

    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Run the app
if __name__ == '__main__':
    app.run()
