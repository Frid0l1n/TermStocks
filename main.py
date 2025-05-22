import yfinance as yf

class Color:
        def __init__(self):
                self.RED = '\033[91m'
                self.GREEN = '\033[92m'
                self.reset = '\033[0m'
        def colorize(self, text, color):
              color_code = getattr(self, color.upper(), '')
              return f"{color_code}{text}{self.reset}"
        

colors = Color()


stocks = [
    "SLHN.SW",
    "ZURN.SW",
    "SREN.SW",
    "NOVN.SW",
    "HOLN.SW",
    "NESN.SW",
    "UHR.SW"
]

for symbol in stocks:
    ticker = yf.Ticker(symbol)
    data = ticker.history(period="1d", interval="1m")
    
    if not data.empty:
        open_price = data.iloc[0]['Open']
        latest_price = data.iloc[-1]['Close']
        change_percent = ((latest_price - open_price) / open_price) * 100
        price_difference = latest_price - open_price

        line = f"{symbol.ljust(8)} Open: {open_price:8.2f}  Now: {latest_price:8.2f}  Change: {change_percent:6.2f}%  Price Change: {price_difference:7.2f}"

        if price_difference > 0:
              print(colors.colorize(line, "GREEN"))
        elif price_difference < 0:
              print(colors.colorize(line, "RED"))
        else:
              print(f"{symbol} - No intraday data available.")