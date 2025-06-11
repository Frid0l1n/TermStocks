import yfinance as yf
from collections import defaultdict
# Transactions: (Stock, Price per Unit, Quantity, Fees)
transactions = [
    ("ZURN", 600, 0.666, 2.3),
    ("ZURN", 559.8, 0.5359, 1.75),
    ("NOVN", 91.26, 0.8091, 1.05),
    ("NOVN", 91.14, 0.9875, 1.05),
    ("HOLM", 93.4, 1.0707, 1.1),
    ("HOLM", 88.12, 1.8157, 1.1),
    ("UHRN", 162.65, 1, 1.1),
    ("SLHN", 825.8, 0.1453, 1.1),
    ("SLHN", 755, 0.0662, 1.05),
    ("SLHN", 793.2, 0.5043, 2.3),
    ("SLHN", 756.4, 0.2644, 1.15),
    ("SREN", 138.2, 1.7945, 1.45),
    ("SREN", 122.6, 1.2235, 1.1),
    ("NESN", 89.12, 1.3465, 0.1),
    ("NESN", 77.76, 1.286, 1.1),
    ("NESN", 74.8, 2.0053, 1.1),
]

# Replace with current market prices for each stock
tickers = {
    "ZURN": "ZURN.SW",
    "NOVN": "NOVN.SW",
    "HOLM": "HOLN.SW",
    "UHRN": "UHR.SW",
    "SLHN": "SLHN.SW",
    "SREN": "SREN.SW",
    "NESN": "NESN.SW",
}

# Fetch current prices
current_prices = {}
for stock, ticker in tickers.items():
    data = yf.Ticker(ticker).history(period="1d")
    if not data.empty:
        current_prices[stock] = data["Close"].iloc[-1]
    else:
        print(f"Warning: No data for {ticker}")
        current_prices[stock] = None

print("Current Prices:")
for stock, price in current_prices.items():
    print(f"{stock}: {price:.2f} CHF" if price else f"{stock}: Price not available")

costs = defaultdict(float)
quantities = defaultdict(float)

# Aggregate costs and quantities
for stock, price, qty, fee in transactions:
    costs[stock] += price * qty + fee
    quantities[stock] += qty

# Calculate profits
profits = {}
total_profit = 0

for stock in costs:
    current_value = current_prices[stock] * quantities[stock]
    profit = current_value - costs[stock]
    profits[stock] = profit
    total_profit += profit

# Output
for stock, profit in profits.items():
    print(f"{stock}: Profit = {profit:.2f} CHF")

print(f"\nTotal Profit: {total_profit:.2f} CHF")
