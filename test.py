import numpy as np
import matplotlib.pyplot as plt

def generate_stock_data(days=10000, start_price=100, volatility=1):
    """
    Generate continuous stock-like data using a random walk model.
    
    Parameters:
        days (int): Number of days to simulate.
        start_price (float): Starting price of the stock.
        volatility (float): Determines the variability in daily price changes.
    
    Returns:
        np.ndarray: Array of simulated stock prices.
    """
    prices = [start_price]
    for _ in range(1, days):
        daily_change = np.random.normal(0, volatility) 
        new_price = max(prices[-1] + daily_change, 0)  # Prevent negative stock price
        prices.append(new_price)
    
    return np.array(prices)

# Parameters
days = 1000       # Number of days
start_price = 100  # Starting stock price
volatility = 2     # Controls the variability in daily price changes

# Generate stock data
stock_prices = generate_stock_data(days, start_price, volatility)

# Plotting
plt.figure(figsize=(12, 6))
plt.plot(stock_prices, color="blue", label="Simulated Stock Price")
plt.title("Simulated Stock Price Over Time")
plt.xlabel("Days")
plt.ylabel("Price")
plt.legend()
plt.grid(True)
plt.show()
