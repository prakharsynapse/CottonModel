from flask import Flask, render_template, request, jsonify
import numpy as np
import pandas as pd
import datetime as dt
from tensorflow.keras.models import load_model
from sklearn.preprocessing import MinMaxScaler
import matplotlib.pyplot as plt

# Initialize Flask app
app = Flask(__name__)

import pickle

# Load the pre-trained model
with open('model2.pkl', 'rb') as file:
    model = pickle.load(file)


# Load and preprocess dataset
market = pd.read_csv("merged_agmarknet_adoni_market.csv")
kapas = market.loc[market['Variety'] == 'Kapas (Adoni)']
kapas = kapas[['Arrival_Date', 'Modal Price']]

# Filter dataset from 2011 onwards and reset index
kapas = kapas.loc[2500:, :]
kapas['Arrival_Date'] = pd.to_datetime(kapas['Arrival_Date'], dayfirst=True)
kapas.set_index('Arrival_Date', inplace=True)
kapas_modal = kapas.iloc[:, -1:].values

# Scale the data
sc = MinMaxScaler(feature_range=(0, 1))
scaled_data = sc.fit_transform(kapas_modal)


# Helper function to predict future prices
def future_prediction(days):
    kapas_modal_future = kapas_modal.copy()
    future_prices = []
    for _ in range(days):
        last_60_days = kapas_modal_future[-60:]
        last_60_days_scaled = sc.transform(last_60_days)
        X_test = np.array([last_60_days_scaled])
        X_test = np.reshape(X_test, (X_test.shape[0], X_test.shape[1], 1))
        pred_price = model.predict(X_test)
        pred_price = sc.inverse_transform(pred_price)
        kapas_modal_future = np.append(kapas_modal_future, pred_price, axis=0)
        future_prices.append(float(pred_price[0][0]))
    return future_prices

@app.route('/')
def home():
    return render_template('index.html')
# Route 1: Prediction endpoint
@app.route('/predict', methods=['GET', 'POST'])
def predict():
    if request.method == 'POST':
        # Get the input date from the user
        input_date = request.form['date']
        current_date = dt.datetime.now().date()

        try:
            input_date = dt.datetime.strptime(input_date, "%Y-%m-%d").date()
            days = (input_date - current_date).days

            if days <= 0:
                return jsonify({"error": "Prediction date must be in the future."})

            # Predict future prices
            predictions = future_prediction(days)

            # Format results
            result = {
                "Prediction Start Date": str(current_date + dt.timedelta(days=1)),
                "Prediction End Date": str(input_date),
                "Predicted Prices": predictions,
            }
            return jsonify(result)

        except ValueError:
            return jsonify({"error": "Invalid date format. Use YYYY-mm-dd."})

    return render_template('predict.html')


# Route 2: Real vs Predicted Accuracy
@app.route('/modelacc', methods=['GET'])
def model_accuracy():
    # Split dataset into train and test sets (last 20%)
    train_size = int(len(scaled_data) * 0.8)
    test_data = scaled_data[train_size - 60:]
    test_prices = kapas_modal[train_size:]

    # Prepare test set
    X_test = []
    for i in range(60, len(test_data)):
        X_test.append(test_data[i - 60:i, 0])
    X_test = np.array(X_test)
    X_test = np.reshape(X_test, (X_test.shape[0], X_test.shape[1], 1))

    # Predictions
    predicted_prices = model.predict(X_test)
    predicted_prices = sc.inverse_transform(predicted_prices)

    # Plot Real vs Predicted Prices
    plt.figure(figsize=(10, 6))
    plt.plot(test_prices, color='green', label='Real Modal Price')
    plt.plot(predicted_prices, color='red', label='Predicted Modal Price')
    plt.title('Real vs Predicted Modal Prices')
    plt.xlabel('Days')
    plt.ylabel('Price (INR)')
    plt.legend()
    plt.savefig('static/accuracy_plot.png')
    plt.close()

    return render_template('modelacc.html', plot_url='/static/accuracy_plot.png')


# Route 3: Future Price Trend
@app.route('/charts', methods=['GET'])
def future_trend():
    # Generate future predictions for 30 days
    future_days = 30
    future_prices = future_prediction(future_days)
    future_dates = [(dt.datetime.now().date() + dt.timedelta(days=i + 1)) for i in range(future_days)]

    # Plot Future Price Trend
    plt.figure(figsize=(10, 6))
    plt.plot(future_dates, future_prices, color='blue', label='Predicted Prices')
    plt.title('Future Cotton Prices Trend')
    plt.xlabel('Date')
    plt.ylabel('Price (INR)')
    plt.xticks(rotation=45)
    plt.legend()
    plt.tight_layout()
    plt.savefig('static/future_trend.png')
    plt.close()

    return render_template('charts.html', plot_url='/static/future_trend.png')


# Main entry point
if __name__ == '__main__':
    app.run(debug=True)
    