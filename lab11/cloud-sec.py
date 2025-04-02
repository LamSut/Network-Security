import dash
from dash import dcc, html
import plotly.graph_objs as go
from flask import Flask
import time
import numpy as np
import tensorflow as tf

# Flask server
server = Flask(__name__)

# Dash app
app = dash.Dash(__name__, server=server, routes_pathname_prefix='/dashboard/')

# Load or create AI model for risk analysis
model = tf.keras.models.Sequential([
    tf.keras.layers.Dense(16, activation='relu', input_shape=(4,)),
    tf.keras.layers.Dense(8, activation='relu'),
    tf.keras.layers.Dense(1, activation='sigmoid')
])
model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])

# Simulated risk assessment function using AI
def analyze_hacking_risk():
    data = np.random.rand(1, 4)
    risk_score = model.predict(data)[0][0] * 100
    return {
        "CPU Usage": data[0][0] * 100,
        "Unauthorized Access Attempts": data[0][1] * 10,
        "Anomalous Traffic": data[0][2] * 100,
        "Malicious Requests": data[0][3] * 50,
        "AI Risk Score": risk_score
    }

# Store risk data
risk_data = []

# Dash layout
app.layout = html.Div([
    html.H1("AI-Driven Cloud Server Hacking Risk Dashboard"),
    dcc.Interval(id='interval-update', interval=5000, n_intervals=0),  # Update every 5 seconds
    dcc.Graph(id='risk-graph')
])

# Callback to update risk data and graph
@app.callback(
    dash.dependencies.Output('risk-graph', 'figure'),
    [dash.dependencies.Input('interval-update', 'n_intervals')]
)
def update_graph(n):
    global risk_data
    risk_data.append(analyze_hacking_risk())
    if len(risk_data) > 10:
        risk_data.pop(0)

    latest_data = risk_data[-1]
    categories = list(latest_data.keys())
    values = list(latest_data.values())

    fig = go.Figure([go.Bar(x=categories, y=values)])
    fig.update_layout(title="AI-Driven Hacking Risk Factors",
                      xaxis_title="Factors",
                      yaxis_title="Severity")
    return fig

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8050)

