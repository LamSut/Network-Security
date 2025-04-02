import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import plotly.graph_objs as go
import pandas as pd
import numpy as np
import time

# Initialize the Dash app
app = dash.Dash(__name__)

# Sample IoT server data (simulated)
servers = [f"IoT_Server_{i}" for i in range(1, 11)]

def generate_security_data():
    """ Simulates AI-based security risk scores with additional metrics."""
    return pd.DataFrame({
        "Server": servers,
        "Risk Score": np.random.randint(10, 100, size=len(servers)),
        "Anomalies Detected": np.random.randint(0, 15, size=len(servers)),
        "CPU Load (%)": np.random.uniform(20, 95, size=len(servers)),
        "Network Traffic (MB)": np.random.uniform(100, 1000, size=len(servers))
    })

# Layout of the dashboard
app.layout = html.Div([
    html.H1("AI-Driven IoT Server Security Dashboard", style={'textAlign': 'center'}),
    dcc.Interval(id='interval-component', interval=5000, n_intervals=0),  # Auto refresh every 5 sec
    dcc.Graph(id='security-status-graph'),
])

@app.callback(
    Output('security-status-graph', 'figure'),
    [Input('interval-component', 'n_intervals')]
)
def update_graph(n):
    df = generate_security_data()
    print("Generated Data:")  # Debug log
    print(df)
    fig = go.Figure()
    fig.add_trace(go.Bar(x=df['Server'], y=df['Risk Score'], name='Risk Score', marker_color='red'))
    fig.add_trace(go.Scatter(x=df['Server'], y=df['Anomalies Detected'], name='Anomalies', mode='markers',
                             marker=dict(size=10, color='blue')))
    fig.add_trace(go.Scatter(x=df['Server'], y=df['CPU Load (%)'], name='CPU Load (%)', mode='lines',
                             line=dict(color='green')))
    fig.add_trace(go.Scatter(x=df['Server'], y=df['Network Traffic (MB)'], name='Network Traffic (MB)', mode='lines',
                             line=dict(color='purple')))
    fig.update_layout(title='IoT Server Security Status', xaxis_title='Server', yaxis_title='Score',
                      barmode='group')
    return fig

if __name__ == '__main__':
    app.run_server(debug=False, port=8060)
