import numpy as np
import pandas as pd
from sklearn.ensemble import IsolationForest
from sklearn.preprocessing import StandardScaler
import matplotlib.pyplot as plt
import smtplib

# Step 1: Data Collection (Simulated for demonstration)
def load_data():
    # Simulate IoT server data: time, CPU, memory, network traffic
    np.random.seed(42)
    data = {
        'time': pd.date_range(start='2023-01-01', periods=1000, freq='H'),
        'cpu_usage': np.random.normal(50, 10, 1000),
        'memory_usage': np.random.normal(60, 15, 1000),
        'network_traffic': np.random.normal(300, 50, 1000),
    }
    return pd.DataFrame(data)

data = load_data()

# Step 2: Preprocessing
def preprocess_data(df):
    scaler = StandardScaler()
    features = ['cpu_usage', 'memory_usage', 'network_traffic']
    df[features] = scaler.fit_transform(df[features])
    return df, scaler

data, scaler = preprocess_data(data)

# Step 3: Anomaly Detection Model
def train_anomaly_detector(df):
    model = IsolationForest(contamination=0.05, random_state=42)
    features = ['cpu_usage', 'memory_usage', 'network_traffic']
    model.fit(df[features])
    df['anomaly_score'] = model.decision_function(df[features])
    df['is_anomaly'] = model.predict(df[features])
    return model, df

model, data = train_anomaly_detector(data)

# Step 4: Risk Scoring and Alerts
def detect_risks(df):
    anomalies = df[df['is_anomaly'] == -1]
    print(f"Detected {len(anomalies)} anomalies out of {len(df)} samples.")
    return anomalies

def send_alert(anomalies):
    if len(anomalies) > 0:
        # Example email alert (customize as needed)
        server = smtplib.SMTP('smtp.example.com', 587)
        server.starttls()
        server.login('your_email@example.com', 'password')
        message = f"Subject: IoT Server Risk Alert\n\nDetected {len(anomalies)} anomalies. Check immediately."
        server.sendmail('your_email@example.com', 'recipient@example.com', message)
        server.quit()

anomalies = detect_risks(data)
send_alert(anomalies)

# Step 5: Visualization
def plot_anomalies(df):
    plt.figure(figsize=(15, 6))
    plt.plot(df['time'], df['cpu_usage'], label='CPU Usage')
    plt.scatter(df['time'][df['is_anomaly'] == -1], df['cpu_usage'][df['is_anomaly'] == -1], color='red', label='Anomalies')
    plt.legend()
    plt.title('IoT Server Risk Detection')
    plt.show()

plot_anomalies(data)