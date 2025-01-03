# Financial Prediction Quantum Neural Network (QNN) App

> [!IMPORTANT]
**This is my solution for [UoB Quantum Hackathon](https://github.com/TumCucTom/bristol-quantum-hackathon-async)**

This repository contains the code and resources for a Quantum Neural Network (QNN) app aimed at financial prediction. The app leverages quantum computing principles combined with machine learning to analyze financial data and make predictions.

You'll find:
- Code:
  - Frontend [web app](frontend/quantum-finance-predictions)
  - Backend [server](server)
  - [Network training](QNN)
  - [Data prep](data)
- Documentation
  - Here
  - Reproduce / walkthrough [jupyter notebooks](notebooks)
  - Report [raw](report.tex) and [pdf](report.pdf)

## Features

- **Quantum Neural Network Model**: Uses quantum computing to enhance the prediction accuracy in financial markets.
- **Financial Data Analysis**: Capable of processing historical stock data, currency exchange rates, and other financial time series.
- **Prediction Output**: Provides prediction probabilities for stock prices, trends, or other financial indicators.
- **Jupyter Notebooks**: Interactive notebooks for demonstrating the training and evaluation of the QNN model, as well as testing on various financial datasets.
- **Modular Architecture**: Easily extendable for other types of data or prediction models.

## Requirements

To run the app locally, make sure you have the following dependencies installed:

- Python 3.8 or higher
- Jupyter Notebook
- [Qiskit](https://qiskit.org/): Quantum computing framework for running quantum algorithms
- [TensorFlow](https://www.tensorflow.org/): Deep learning framework for building and training the QNN model
- Flask or Django for the backend
- Vue.js for the frontend
- Plotly for visualizations
- Other Python dependencies (listed in `requirements.txt`)

## Installation Steps

1. **Clone the Repository**:
    ```bash
    git clone https://github.com/TumCucTom/quantum-finance-predictions.git
    cd quantum-finance-predictions
    ```

2. **Create a Virtual Environment**:
    ```bash
    python -m venv venv
    source venv/bin/activate  # For macOS/Linux
    venv\Scripts\activate     # For Windows
    ```

3. **Install the Dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

4. **Start Jupyter Notebook**:
    ```bash
    jupyter lab
    ```

5. **Open the `xx.ipynb` notebooks** to build your own version of the model.

## Project Workflow

Creating the Quantum Neural Network (QNN)-powered stock market prediction web app involves several stages:

### 1. Project Planning & Setup
- **Define Scope**: Determine core features and functionality, such as data input, prediction capabilities, and visualizations.
- **Select Tools & Tech Stack**:
   - **Quantum Libraries**: PennyLane, Qiskit
   - **Backend**: Python (Flask or Django)
   - **Frontend**: React or Vue.js for interactive UI
   - **Visualization**: Plotly, D3.js
   - **Data Sources**: Alpha Vantage API, Yahoo Finance, Binance API
   - **Hosting**: AWS, Google Cloud, or Heroku

### 2. Data Collection & Preprocessing
- **Stock Data Collection**:
   - Fetch historical stock data using APIs (e.g., Alpha Vantage, Yahoo Finance).
   - Allow users to upload their own CSV files with historical data.
- **Data Preprocessing**:
   - Clean data by handling missing values and scaling/normalizing the data.
   - Format the data for use in the QNN model.
   - Split data into training, validation, and test sets.

### 3. Quantum Neural Network Model Development
- **Set Up Quantum Computing Framework**:
   - Install PennyLane or Qiskit.
   - Set up a basic QNN using quantum layers and variational parameters.
- **Model Design**:
   - Define the QNN architecture using quantum circuits and classical-quantum hybrid systems.
- **Training the Model**:
   - Implement a hybrid training approach with classical optimizers and quantum circuits.
   - Train the model using prepared stock data and evaluate its performance.
- **Prediction Logic**:
   - Once trained, use the QNN model to predict future stock prices based on historical data.

### 4. Backend Development
- **Setup Flask or Django**:
   - Build the backend API to handle requests for stock data, model predictions, and file uploads.
- **Integrate Quantum Model**:
   - Use the trained QNN model to process data and return predictions for stock prices.
- **Data Handling**:
   - Implement routes for file uploads and fetching stock data from external APIs.

### 5. Frontend Development
- **Design the UI**:
   - Use React or Vue.js to build an interactive frontend.
   - Display charts and graphs with Plotly or D3.js to visualize stock price data and predictions.
- **Stock Data Display**:
   - Allow users to select different stocks or cryptocurrencies and view historical data and predictions.
- **User Interaction**:
   - Create features like file uploads, prediction buttons, and dropdowns for selecting prediction timeframes.

### 6. Deployment
- **Integrate Frontend & Backend**:
   - Ensure proper communication between the frontend and backend through HTTP requests.
- **Deploy to the Cloud**:
   - Host the app on AWS, Google Cloud, or Heroku for scalability.
- **Real-time Data & Prediction**:
   - Set up real-time stock data fetching and prediction updates.

### 7. Testing & Iteration
- **Test Model Accuracy**:
   - Compare predictions with actual market data.
   - Use traditional models (e.g., LSTM, ARIMA) as baselines for comparison.
- **User Testing**:
   - Gather feedback from real users to improve the UI/UX.
- **Optimization**:
   - Optimize the QNN for speed and accuracy.

### 8. Final Touches
- **Add Documentation**:
   - Document how users can interact with the app and use the QNN model.
- **Provide Tutorials**:
   - Offer tutorials on how to use the app and interpret the results.
- **Prepare for Scale**:
   - Ensure the backend can handle high traffic and scale when needed.

### 9. Future Improvements
- **Quantum Hardware Integration**:
   - As quantum hardware becomes available, consider shifting to actual quantum processors.
- **Advanced Predictions**:
   - Implement multi-step forecasting, sentiment analysis, and use alternative financial indicators.

## Usage

- After setting up the environment, you can run the project using the vue app and backend server or:
- The [notebooks](notebooks) provide step-by-step instructions for training the model on financial data and making predictions.
- Modify the input data in the provided cells to test the model with your own datasets.

## License

This project is licensed under the [MIT License](LICENSE).
