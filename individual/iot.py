import numpy as np
import pandas as pd
from sklearn.ensemble import IsolationForest
from sklearn.preprocessing import MinMaxScaler
import matplotlib.pyplot as plt
import smtplib

import os
from dotenv import load_dotenv
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders

# Load environment variables
load_dotenv()
email = os.getenv('mail')
password = os.getenv('pass')

# Step 1: Data Collection (Simulated for demonstration)
def load_data():
    np.random.seed(42)
    data = {
        'time': pd.date_range(start='2024-01-01', periods=500, freq='h'),
        'cpu_usage': np.random.normal(55, 45, 500),
        'memory_usage': np.random.normal(65, 35, 500),
        'network_traffic': np.random.normal(1000, 1000, 500),
    }
    return pd.DataFrame(data)

data = load_data()

# Step 2: Preprocessing (Normalize to range -1 to 1)
def preprocess_data(df):
    scaler = MinMaxScaler(feature_range=(-1, 1))
    features = ['cpu_usage', 'memory_usage', 'network_traffic']
    df[features] = scaler.fit_transform(df[features])
    return df, scaler

data, scaler = preprocess_data(data)

# Step 3: Anomaly Detection Model with >0 logic
def train_anomaly_detector_with_positive_check(df):
    model = IsolationForest(contamination='auto', random_state=42)
    features = ['cpu_usage', 'memory_usage', 'network_traffic']
    model.fit(df[features])
    df['anomaly_score'] = model.decision_function(df[features])
    df['is_anomaly'] = model.predict(df[features])
    
    df['is_anomaly'] = df.apply(
        lambda row: -1 if (row['is_anomaly'] == -1 and 
                           (row['cpu_usage'] > 0.5 or row['memory_usage'] > 0.7 or row['network_traffic'] > 0.9))
        else 1, axis=1
    )
    return model, df

model, data = train_anomaly_detector_with_positive_check(data)

# Step 4: Visualization and Save Figures
def plot_and_save_anomalies(df):
    cpu_anomalies = df[(df['is_anomaly'] == -1) & (df['cpu_usage'] > 0.5)]
    memory_anomalies = df[(df['is_anomaly'] == -1) & (df['memory_usage'] > 0.7)]
    network_anomalies = df[(df['is_anomaly'] == -1) & (df['network_traffic'] > 0.9)]
    
    # CPU Anomalies
    plt.figure(figsize=(10, 4))
    plt.plot(df['time'], df['cpu_usage'], label='CPU Usage (normalized)')
    plt.scatter(cpu_anomalies['time'], cpu_anomalies['cpu_usage'], color='red', label='Anomalies > 0')
    plt.legend()
    plt.title('CPU Usage Anomalies')
    plt.xlabel('Time')
    plt.ylabel('CPU Usage')
    plt.savefig('cpu_anomalies.png')
    plt.close()
    
    # Memory Anomalies
    plt.figure(figsize=(10, 4))
    plt.plot(df['time'], df['memory_usage'], label='Memory Usage (normalized)')
    plt.scatter(memory_anomalies['time'], memory_anomalies['memory_usage'], color='red', label='Anomalies > 0')
    plt.legend()
    plt.title('Memory Usage Anomalies')
    plt.xlabel('Time')
    plt.ylabel('Memory Usage')
    plt.savefig('memory_anomalies.png')
    plt.close()
    
    # Network Traffic Anomalies
    plt.figure(figsize=(10, 4))
    plt.plot(df['time'], df['network_traffic'], label='Network Traffic (normalized)')
    plt.scatter(network_anomalies['time'], network_anomalies['network_traffic'], color='red', label='Anomalies > 0')
    plt.legend()
    plt.title('Network Traffic Anomalies')
    plt.xlabel('Time')
    plt.ylabel('Network Traffic')
    plt.savefig('network_anomalies.png')
    plt.close()

plot_and_save_anomalies(data)

# Step 5: Send Email with Attached Figures
def send_email_with_attachments():
    msg = MIMEMultipart()
    msg['From'] = email
    msg['To'] = email
    msg['Subject'] = "IoT Server Risk Alert with Anomaly Figures"
    
    body = "Attached are the anomaly figures detected in the IoT server data. Please review them."
    msg.attach(MIMEText(body, 'plain'))
    
    attachments = ['cpu_anomalies.png', 'memory_anomalies.png', 'network_anomalies.png']
    
    for file in attachments:
        with open(file, 'rb') as attachment:
            part = MIMEBase('application', 'octet-stream')
            part.set_payload(attachment.read())
            encoders.encode_base64(part)
            part.add_header('Content-Disposition', f'attachment; filename={file}')
            msg.attach(part)
    
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(email, password)
    server.send_message(msg)
    server.quit()
    print("Email with anomaly figures sent successfully!")

send_email_with_attachments()
