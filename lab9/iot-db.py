import sqlite3
import pandas as pd
import numpy as np
from sklearn.preprocessing import MinMaxScaler
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense

# Ensure the database and table exist
def initialize_database():
    conn = sqlite3.connect('iot_data.db')
    cursor = conn.cursor()
    
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS sensor_data (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            temperature REAL,
            humidity REAL,
            timestamp TEXT
        )
    """)
    conn.commit()
    conn.close()

# Insert test data if the table is empty
def insert_test_data():
    conn = sqlite3.connect('iot_data.db')
    cursor = conn.cursor()
    
    cursor.execute("SELECT COUNT(*) FROM sensor_data")
    count = cursor.fetchone()[0]
    
    if count == 0:  # Insert sample data only if table is empty
        sample_data = [
            (25.3, 60.5, '2025-03-18 12:00:00'),
            (26.1, 58.2, '2025-03-18 12:05:00'),
            (24.8, 62.1, '2025-03-18 12:10:00'),
            (23.7, 64.0, '2025-03-18 12:15:00'),
            (27.0, 55.8, '2025-03-18 12:20:00'),
            (26.5, 57.1, '2025-03-18 12:25:00')
        ]
        cursor.executemany("INSERT INTO sensor_data (temperature, humidity, timestamp) VALUES (?, ?, ?)", sample_data)
        conn.commit()
    
    conn.close()

# Load data from the IoT database
def load_data():
    conn = sqlite3.connect('iot_data.db')
    query = "SELECT temperature, humidity, timestamp FROM sensor_data ORDER BY timestamp ASC"
    df = pd.read_sql_query(query, conn)
    conn.close()
    
    if df.empty:
        raise ValueError("No data found in sensor_data table. Please check your database.")
    
    return df

# Preprocessing
def preprocess_data(df):
    df['timestamp'] = pd.to_datetime(df['timestamp'])
    df.sort_values(by='timestamp', inplace=True)
    
    scaler = MinMaxScaler(feature_range=(0, 1))
    scaled_data = scaler.fit_transform(df[['temperature', 'humidity']])
    
    X, y = [], []
    seq_length = 5  # Past 5 data points to predict the next
    
    for i in range(len(scaled_data) - seq_length):
        X.append(scaled_data[i:i+seq_length])
        y.append(scaled_data[i+seq_length])
    
    return np.array(X), np.array(y), scaler

# AI Model (LSTM)
def build_lstm_model(input_shape):
    model = Sequential([
        LSTM(50, return_sequences=True, input_shape=input_shape),
        LSTM(50),
        Dense(2)
    ])
    model.compile(optimizer='adam', loss='mse')
    return model

# Main execution
initialize_database()
insert_test_data()
df = load_data()

X, y, scaler = preprocess_data(df)
model = build_lstm_model(X.shape[1:])
model.fit(X, y, epochs=10, batch_size=16, verbose=1)

# Predict the next sensor data
next_prediction = model.predict(np.expand_dims(X[-1], axis=0))
predicted_values = scaler.inverse_transform(next_prediction)
print("Predicted next values:", predicted_values)
.
