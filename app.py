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
CORS(app)  # Enable CORS for your Flask app

# List of solar energy brands and their symbols
solar_brands = ["FSLR", "SPWR", "ENPH", "CSIQ", "RUN", "NOVA", "NEE", "SEDG"]

# Dictionary to store Dash apps and data for each solar brand
dash_apps = {}
solar_data = {}

# Initialize data for each solar brand
for brand in solar_brands:
    X = deque(maxlen=20)
    X.append(1)
    Y = deque(maxlen=20)
    Y.append(100)  # Initial brand price

    open_prices = deque(maxlen=20)
    high_prices = deque(maxlen=20)
    low_prices = deque(maxlen=20)
    close_prices = deque(maxlen=20)
    open_prices.append(Y[-1])
    high_prices.append(Y[-1])
    low_prices.append(Y[-1])
    close_prices.append(Y[-1])

    solar_data[brand] = {
        'X': X,
        'Y': Y,
        'open_prices': open_prices,
        'high_prices': high_prices,
        'low_prices': low_prices,
        'close_prices': close_prices,
    }

    # Initialize a Dash app for each solar brand
    dash_app = dash.Dash(__name__, server=app, url_base_pathname=f'/graph/{brand}/')

    dash_app.layout = html.Div([
        html.H3(f'Live Solar Brand Price Fluctuation: {brand}'),
        dcc.Graph(id=f'live-graph-{brand}', animate=True),
        dcc.Interval(
            id=f'graph-update-{brand}',
            interval=1000,  # Update every second
            n_intervals=0
        ),
    ])

    # Callback for each brand's live graph
    @dash_app.callback(
        Output(f'live-graph-{brand}', 'figure'),
        [Input(f'graph-update-{brand}', 'n_intervals')]
    )
    def update_graph_scatter(n, brand=brand):
        # Get brand-specific data
        data = solar_data[brand]
        X, Y = data['X'], data['Y']
        open_prices, high_prices, low_prices, close_prices = data['open_prices'], data['high_prices'], data['low_prices'], data['close_prices']

        # Generate new random price data
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

        # Graph data
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
                    tickmode="array",
                    tickvals=list(range(min(X), max(X) + 1, 2)),
                ),
                yaxis=dict(range=[min(low_prices), max(high_prices)]),
                title=f'Live Price Fluctuations - {brand}'
            )
        }

    # Save Dash app to dictionary for easy access
    dash_apps[brand] = dash_app

# Flask route to serve the dashboard page
@app.route('/dashboard', methods=['GET'])
@app.route('/dashboard/<string:stock_symbol>', methods=['GET'])
def dashboard(stock_symbol=None):
    return render_template('dashboard.html', stock_symbol=stock_symbol)

# Flask route for login
@app.route('/')
def login():
    return render_template('index.html')

@app.route('/save-user', methods=['POST'])
def save_user():
    data = request.json
    user_id = data.get('userID')
    user_name = data.get('userName')
    user_photo = data.get('userPhoto')

    if not user_id:
        return jsonify({"error": "UserID is required"}), 400

    filename = f"static/users/{user_id}.json"
    filepath = os.path.join(filename)
    
    os.makedirs("users_data", exist_ok=True)

    user_data = {
        "userID": user_id,
        "userName": user_name,
        "userPhoto": user_photo
    }

    with open(filepath, "w") as file:
        json.dump(user_data, file, indent=4)

    print(f"User data for {user_name} (ID: {user_id}) has been saved to {filename}")
    return jsonify({"message": "User data saved successfully"}), 200

@app.route('/test')
def test():
    return "Server is running"


if __name__ == '__main__':
    app.run(host='localhost', port=5000, debug=True)
    app.wsgi_app = DispatcherMiddleware(app.wsgi_app, {'/dash': dash_app.server})
    app.run(debug=True)
