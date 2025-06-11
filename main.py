import yfinance as yf
from rich.console import Console
from rich.table import Table
from rich.text import Text
import time
import os

def get_stock_performance():
    stocks = [
        "SLHN.SW", "ZURN.SW", "SREN.SW", "NOVN.SW",
        "HOLN.SW", "NESN.SW", "UHR.SW"
    ]
    data_results = {}

    for symbol in stocks:
        try:
            ticker = yf.Ticker(symbol)
            data = ticker.history(period="1d", interval="1m")

            if not data.empty:
                open_price = data.iloc[0]['Open']
                latest_price = data.iloc[-1]['Close']
                change_percent = ((latest_price - open_price) / open_price) * 100
                price_difference = latest_price - open_price

                data_results[symbol] = {
                    "open": open_price,
                    "now": latest_price,
                    "change_percent": change_percent,
                    "price_difference": price_difference
                }
            else:
                data_results[symbol] = None
        except Exception as e:
            print(f"Error fetching data for {symbol}: {e}", file=os.sys.stderr)
            data_results[symbol] = None

    return data_results

def create_stock_table(stocks_data: dict) -> Table:
    table = Table(title="Portfolio Performance", expand=True)
    table.add_column("Symbol", style="bold")
    table.add_column("Open", justify="right")
    table.add_column("Now", justify="right")
    table.add_column("Change %", justify="right")
    table.add_column("Δ Price", justify="right")

    if not stocks_data:
        table.add_row(Text("No stock data available.", style="red", justify="center"), "", "", "", "")
        return table

    for symbol, data in stocks_data.items():
        if data:
            open_price = data['open']
            latest_price = data['now']
            change_percent = data['change_percent']
            price_difference = data['price_difference']

            if price_difference > 0:
                change_str = Text(f"{change_percent:6.2f}%", style="green")
                price_diff_str = Text(f"{price_difference:7.2f}", style="green")
            elif price_difference < 0:
                change_str = Text(f"{change_percent:6.2f}%", style="red")
                price_diff_str = Text(f"{price_difference:7.2f}", style="red")
            else:
                change_str = Text(f"{change_percent:6.2f}%")
                price_diff_str = Text(f"{price_difference:7.2f}")

            table.add_row(
                symbol,
                f"{open_price:8.2f}",
                f"{latest_price:8.2f}",
                change_str,
                price_diff_str
            )
        else:
            table.add_row(symbol, "-", "-", Text("No data", style="red"), Text("No data", style="red"))

    return table

def main():
    console = Console()

    while True:
        console.clear()
        console.print("[bold yellow]Fetching stock data...[/bold yellow]")

        stocks_data = get_stock_performance()
        stock_table = create_stock_table(stocks_data)

        console.clear()
        console.print(stock_table)
        console.print("\n[dim]Press Ctrl+C to exit. Refreshing every 60 seconds...[/dim]")

        try:
            time.sleep(60)
        except KeyboardInterrupt:
            console.print("\n[bold red]Exiting stock tracker.[/bold red]")
            break

if __name__ == "__main__":
    main()