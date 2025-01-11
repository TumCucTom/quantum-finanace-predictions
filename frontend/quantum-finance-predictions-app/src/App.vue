<template>
  <div id="app">
    <header>
      <h1>Quantum Stock Predictor</h1>
    </header>

    <section class="input-section">
      <h2>Upload Stock Data or Fetch by Ticker</h2>
      <div class="file-upload">
        <input type="file" @change="handleFileUpload" />
        <div class="ticker-input">
          <input v-model="ticker" type="text" placeholder="Enter stock ticker (e.g., AAPL)" />
          <button @click="fetchStockData">Fetch Data</button>
        </div>
      </div>
    </section>

    <section class="prediction-section" v-if="stockImage">
      <h2>Stock Data</h2>
      <div class="image-container">
        <img :src="stockImage" alt="Stock Data Graph" class="graph-image" />
      </div>

      <button class="predict-btn" @click="predictStockPrices">Predict Future Prices</button>

      <div v-if="predictionImage">
        <h2>Predicted Prices</h2>
        <div class="image-container">
          <img :src="predictionImage" alt="Predicted Prices Graph" class="graph-image" />
        </div>
      </div>
    </section>

    <!-- Floating Animation in the Bottom Right -->
    <div class="animated-graph-icon">
      <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" width="50" height="50">
        <path fill="none" d="M0 0h24v24H0z"/>
        <path fill="#00aaff" d="M5 3h14c1.1 0 1.99.9 1.99 2L21 19c0 1.1-.89 2-1.99 2H5c-1.1 0-1.99-.9-1.99-2L3 5c0-1.1.89-2 1.99-2zm0 2v14h14V5H5zm7 6h5v2h-5v-2zm0-4h5v2h-5V7zm0 8h5v2h-5v-2z"/>
      </svg>
    </div>
  </div>
</template>

<script>
import axios from "axios";

export default {
  name: "App",
  data() {
    return {
      ticker: "",
      stockImage: "",
      predictionImage: "",
    };
  },
  methods: {
    async loadDefaultData() {
      try {
        const response = await axios.get("http://127.0.0.1:5000/default_stock_image", {
          responseType: "blob",
        });
        this.stockImage = URL.createObjectURL(response.data);
      } catch (error) {
        console.error("Error loading default data image:", error);
      }
    },

    handleFileUpload(event) {
      const file = event.target.files[0];
      const formData = new FormData();
      formData.append("file", file);

      axios
          .post("http://127.0.0.1:5000/predict", formData, {
            headers: { "Content-Type": "multipart/form-data" },
            responseType: "blob",
          })
          .then((response) => {
            this.predictionImage = URL.createObjectURL(response.data);
          })
          .catch((error) => {
            console.error("Error uploading file:", error);
          });
    },

    fetchStockData() {
      if (!this.ticker) {
        alert("Please enter a stock ticker.");
        return;
      }

      axios
          .get(`http://127.0.0.1:5000/fetch_stock_image?ticker=${this.ticker}`, {
            responseType: "blob",
          })
          .then((response) => {
            this.stockImage = URL.createObjectURL(response.data);
          })
          .catch((error) => {
            console.error("Error fetching stock data image:", error);
            alert("An error occurred while fetching the stock data.");
          });
    },

    predictStockPrices() {
      const formData = new FormData();
      formData.append("ticker", this.ticker);

      axios
          .post("http://127.0.0.1:5000/predict_image", formData, {
            headers: { "Content-Type": "multipart/form-data" },
            responseType: "blob",
          })
          .then((response) => {
            this.predictionImage = URL.createObjectURL(response.data);
          })
          .catch((error) => {
            console.error("Error predicting stock prices:", error);
          });
    },
  },
  created() {
    this.loadDefaultData();
  },
};
</script>

<style>

* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

body {
  font-family: 'Roboto', sans-serif;
  background: linear-gradient(135deg, #f7f8fa 50%, #e1f0fe 50%);
  color: #333;
  padding: 30px;
}

header {
  background: linear-gradient(90deg, #0062cc, #00aaff);
  color: white;
  text-align: center;
  padding: 40px 20px;
  border-radius: 12px;
  box-shadow: 0 8px 20px rgba(0, 0, 0, 0.1);
  margin-bottom: 40px;
}

h1 {
  font-size: 36px;
  letter-spacing: 1px;
  margin-bottom: 10px;
}

.input-section, .prediction-section {
  background-color: white;
  border-radius: 12px;
  box-shadow: 0 6px 20px rgba(0, 0, 0, 0.1);
  padding: 30px;
  margin-bottom: 30px;
}

h2 {
  font-size: 26px;
  margin-bottom: 15px;
  color: #0062cc;
}

.file-upload {
  display: flex;
  flex-direction: column;
  gap: 20px;
  margin-bottom: 20px;
}

.ticker-input {
  display: flex;
  align-items: center;
  gap: 15px;
}

input[type="file"] {
  padding: 15px;
  margin-bottom: 20px;
  border: 2px solid #00aaff;
  border-radius: 6px;
  background-color: #fff;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
  transition: transform 0.2s ease-in-out;
}

input[type="file"]:hover {
  transform: scale(1.05);
}

input[type="text"] {
  padding: 15px;
  border: 2px solid #00aaff;
  border-radius: 6px;
  width: 250px;
  transition: box-shadow 0.3s ease;
}

input[type="text"]:focus {
  box-shadow: 0 0 8px 2px rgba(0, 170, 255, 0.7);
}

button {
  background-color: #00aaff;
  color: white;
  border: none;
  padding: 14px 24px;
  cursor: pointer;
  border-radius: 8px;
  transition: background-color 0.3s, transform 0.2s ease;
}

button:hover {
  background-color: #007bb2;
  transform: scale(1.05);
}

.predict-btn {
  margin-top: 20px;
  padding: 14px 30px;
  font-weight: bold;
}

.plotly-chart {
  margin: 30px 0;
}

.animated-graph-icon {
  position: fixed;
  bottom: 20px;
  right: 20px;
  animation: float 2s ease-in-out infinite;
}

@keyframes float {
  0% {
    transform: translateY(0);
  }
  50% {
    transform: translateY(-10px);
  }
  100% {
    transform: translateY(0);
  }
}

@media (max-width: 768px) {
  .ticker-input {
    flex-direction: column;
    align-items: flex-start;
  }

  .file-upload {
    align-items: center;
  }

  .input-section, .prediction-section {
    padding: 20px;
  }
}

.graph-image {
  max-width: 100%;
  border-radius: 12px;
  box-shadow: 0 4px 10px rgba(0, 0, 0, 0.2);
  margin-bottom: 20px;
}

</style>
