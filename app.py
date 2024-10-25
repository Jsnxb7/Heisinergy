from flask import Flask, request, jsonify, redirect, url_for, render_template, make_response
from flask_cors import CORS
from werkzeug.security import check_password_hash, generate_password_hash
import os
import json
from dash import dcc, html
import plotly.graph_objs as go
import random
from collections import deque
from dash.dependencies import Output, Input
from flask import Flask, render_template
from werkzeug.middleware.dispatcher import DispatcherMiddleware
import dash

# Flask app setup
app = Flask(__name__)
CORS(app)   

# Setup Dash app to embed within Flask
dash_app = dash.Dash(__name__, server=app, url_base_pathname='/graph/')
dash_app.layout = html.Div([
    dcc.Graph(id='live-graph', animate=True),
    dcc.Interval(
        id='graph-update',
        interval=1000,
        n_intervals=0
    ),
])

# Data for the graph
X = deque(maxlen=20)
X.append(1)
Y = deque(maxlen=20)
Y.append(100)  # Initial stock price

open_prices = deque(maxlen=20)
high_prices = deque(maxlen=20)
low_prices = deque(maxlen=20)
close_prices = deque(maxlen=20)
open_prices.append(Y[-1])
high_prices.append(Y[-1])
low_prices.append(Y[-1])
close_prices.append(Y[-1])

@dash_app.callback(
    Output('live-graph', 'figure'),
    [Input('graph-update', 'n_intervals')]
)
def update_graph_scatter(n):
    new_price = Y[-1] + Y[-1] * random.uniform(-0.05, 0.05)
    X.append(X[-1] + 1)
    Y.append(new_price)

    open_price = close_prices[-1]
    close_price = new_price
    high_price = max(open_price, close_price) * (1 + random.uniform(0, 0.05))
    low_price = min(open_price, close_price) * (1 - random.uniform(0, 0.05))

    open_prices.append(open_price)
    high_prices.append(high_price)
    low_prices.append(low_price)
    close_prices.append(close_price)

    # Save data to JSON
    data_to_save = {
        "X": list(X),
        "Y": list(Y),
        "open": list(open_prices),
        "high": list(high_prices),
        "low": list(low_prices),
        "close": list(close_prices),
    }
    with open("stock_prices.json", "w") as f:
        json.dump(data_to_save, f)

    line_data = go.Scatter(
        x=list(X),
        y=list(Y),
        name='Price Line',
        mode='lines+markers'
    )

    candlestick_data = go.Candlestick(
        x=list(X),
        open=list(open_prices),
        high=list(high_prices),
        low=list(low_prices),
        close=list(close_prices),
        name='Candlestick',
        increasing_line_color='green',
        decreasing_line_color='red'
    )

    return {
        'data': [line_data, candlestick_data],
        'layout': go.Layout(
            xaxis=dict(
                range=[min(X), max(X)],
                tickmode="array",  # Reduce tick labels
                tickvals=list(range(min(X), max(X) + 1, 2)),  # Interval of 2 for fewer tick labels
            ),
            yaxis=dict(range=[min(low_prices), max(high_prices)]),
            title='Live Stock Price Fluctuations with Adjusted Layout'
        )
    }

# Flask route for login
@app.route('/')
def login():
    return render_template('index.html')

@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')

from flask import request, jsonify

@app.route('/save-user', methods=['POST'])
def save_user():
    data = request.json
    user_id = data.get('userID')  # Get the unique user ID
    user_name = data.get('userName')
    user_photo = data.get('userPhoto')
    
    print(f"Received user: {user_name} with ID: {user_id}")
    return jsonify({"message": "User data saved successfully"}), 200


@app.route('/test')
def test():
    return "Server is running"

# Flask route for graph page
@app.route('/graph')
def graph():
    return render_template('graph.html')

if __name__ == '__main__':
    app.run(host='localhost', port=5000, debug=True)
    app.wsgi_app = DispatcherMiddleware(app.wsgi_app, {'/dash': dash_app.server})
    app.run(debug=True)
