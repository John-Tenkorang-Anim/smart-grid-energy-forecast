# smart-grid-energy-forecast

A machine learning-powered platform for forecasting California ISO (CAISO) grid metrics, including carbon intensity, electricity price, and power demand. The project fetches, preprocesses, and models real-world energy data, providing actionable insights for smart grid management and energy optimization.

---

## Table of Contents

- Project Overview
- Features
- Project Structure
- Data Sources
- Installation
- Usage
- Code Modules
- Modeling Approach
- Streamlit App
- Contributing
- License

---

## Project Overview

This project automates the process of:
- Fetching and cleaning CAISO grid data (carbon intensity, price, demand)
- Engineering features and preparing data for modeling
- Training XGBoost models to forecast key grid metrics
- Providing a Streamlit dashboard for interactive exploration and prediction

The goal is to enable smarter energy decisions, reduce carbon footprint, and optimize energy costs.

---

## Features

- **Automated Data Fetching:** Downloads and processes CAISO and US carbon intensity data.
- **Data Preprocessing:** Cleans, interpolates, and engineers time-based and lag features.
- **Model Training:** Trains XGBoost models for multi-target forecasting.
- **Prediction & Optimization:** Predicts future grid metrics and identifies optimal energy usage windows.
- **Interactive Dashboard:** Visualizes forecasts and recommendations via Streamlit.

---

## Project Structure

```
.
├── app.py                      # Streamlit app entry point
├── fetch_data.py               # Data fetching scripts
├── preprocess.py               # Data cleaning and feature engineering
├── model.py                    # Model training, loading, and prediction
├── rl_agent.py                 # (Optional) Reinforcement learning agent
├── requirements.txt            # Python dependencies
├── README.md                   # Project documentation
├── data/
│   ├── us_hourly.csv           # Raw US carbon intensity data
│   └── processed/
│       ├── ca_demand.csv       # Processed CA demand data
│       ├── ca_lmp_prices.csv   # Processed CA price data
│       └── us_carbon_intensity.csv # Processed carbon intensity data
└── models/
    ├── feature_cols_per_model.joblib    # Saved feature columns
    ├── xgb_model_carbonIntensity.joblib # Trained model: carbon intensity
    ├── xgb_model_powerDemand.joblib     # Trained model: power demand
    └── xgb_model_price.joblib           # Trained model: price
```

---

## Data Sources

- **CAISO Market Data:** Real-time and historical grid data via [gridstatus](https://github.com/watt-time/gridstatus).
- **US Carbon Intensity:** Hourly carbon intensity data from public datasets.

---

## Installation

1. **Clone the repository:**
   ```sh
   git clone https://github.com/yourusername/smart-grid-energy-forecast.git
   cd smart-grid-energy-forecast
   ```

2. **Install dependencies:**
   ```sh
   pip install -r requirements.txt
   ```

3. **(Optional) Set up environment variables:**
   - Create a [`.env`](.env ) file for API keys or custom settings if needed.

---

## Usage

### 1. Fetch and Process Data

Run the following to fetch and preprocess all required data:
```sh
python fetch_data.py
python preprocess.py
```

### 2. Train Models

Train the forecasting models:
```sh
python model.py
```

### 3. Launch the Streamlit App

Start the dashboard:
```sh
streamlit run app.py
```

---

## Code Modules

### `fetch_data.py`

- **Purpose:** Downloads and saves raw and processed data.
- **Key Functions:**
  - `fetch_lmp_data()`: Fetches CAISO price data.
  - `fetch_real_ca_demand()`: Fetches CAISO demand data.
  - `fetch_us_carbon_intensity()`: Loads US carbon intensity from CSV.

### `preprocess.py`

- **Purpose:** Cleans, merges, and engineers features from raw data.
- **Key Functions:**
  - `preprocess_data()`: Main function for data cleaning and feature engineering.
  - `create_time_features()`: Adds time-based features (hour, day, etc.).

### `model.py`

- **Purpose:** Trains, saves, loads, and uses XGBoost models for forecasting.
- **Key Functions:**
  - `train_models()`: Trains models for each target variable.
  - `load_models()`: Loads trained models from disk.
  - `predict()`: Generates forecasts.
  - `find_optimal_energy_window()`: Finds best time windows for energy use.
  - `save_feature_cols()` / `load_feature_cols()`: Manage feature column metadata.

### `app.py`

- **Purpose:** Streamlit dashboard for interactive forecasting and visualization.
- **Key Functions:**
  - `load_data()`: Loads preprocessed data.
  - `get_models_and_features()`: Loads models and feature columns.
  - (UI code for visualization and user interaction.)

### `rl_agent.py`

- **Purpose:** (Optional/Experimental) Reinforcement learning agent for advanced optimization.

---

## Modeling Approach

- **Targets:** Carbon intensity, electricity price, power demand.
- **Features:** Time-based (hour, day, etc.), lagged values, engineered features.
- **Models:** XGBoost regressors, one per target.
- **Evaluation:** Trained on historical data, validated on holdout sets.

---
### Model Evaluation and Recommendations

After training, models were evaluated using Mean Absolute Error (MAE), Root Mean Squared Error (RMSE), and the Coefficient of Determination (R²) on the training dataset:

| Target          | MAE     | RMSE    | R²     |
|-----------------|---------|---------|--------|
| powerDemand     | 1145.12 | 1670.81 | 0.89   |
| price           | 2.73    | 4.39    | 0.77   |
| carbonIntensity | 0.14    | 0.16    | 0.00   |

**Interpretation:**

- The **powerDemand** model demonstrates strong predictive accuracy and explains nearly 90% of variance.
- The **price** model shows moderate performance; there is room to improve feature engineering and modeling.
- The **carbonIntensity** model does not effectively capture the variation in carbon intensity, indicating need for better data, features, or modeling approaches.

**Challenges:**
Challenges Faced
- Data Scaling and Units Consistency:
One major challenge was correctly scaling between grid-level data (in MW) and household-level consumption (in kWh). Initial model outputs were unrealistic because of mismatched units, requiring careful normalization and rescaling for meaningful predictions.

- Feature Selection for Multi-Target Models:
Designing separate models for power demand, price, and carbon intensity meant carefully selecting feature sets to avoid data leakage, especially since some features were targets in other models.

- Handling Sparse or Noisy Data:
Electricity price and carbon intensity data often exhibited volatility and occasional gaps, which complicated model training and evaluation. Robust preprocessing and filling missing values was necessary to stabilize results.

- Prediction Accuracy and Error Metrics:
Initial evaluation metrics such as MAE and RMSE appeared very large due to scale issues, prompting implementation of relative error metrics (MAPE and normalized RMSE) for better interpretability.









**Recommendations for future improvements:**

- Enhance feature sets with external data sources (weather, market indicators, grid composition).
- Experiment with advanced machine learning models (ensemble methods, deep learning).
- Implement cross-validation and continuous monitoring for model robustness.
- Consider domain knowledge integration and hybrid physics-ML modeling for carbon intensity.

These steps will improve model reliability and usability for forecasting electricity demand, pricing, and environmental impact at the household level.

## Streamlit App

- **Visualizes:** Forecasts for each target variable.
- **Allows:** User to select time windows, view optimal usage periods, and explore historical trends.
- **Caching:** Uses Streamlit's `@st.cache_data` and `@st.cache_resource` for performance.

---

## Contributing

1. Fork the repo and create your branch.
2. Make your changes and add tests.
3. Submit a pull request.

---

## License

MIT License. See LICENSE for details.

---

## Acknowledgments

- [gridstatus](https://github.com/watt-time/gridstatus) for CAISO data access.
- XGBoost for machine learning models.
- Streamlit for the dashboard framework.

---

**For more details, see the code and comments in


