import yfinance as yf
from textual.app import App, ComposeResult
from textual.widgets import TabbedContent, TabPane, Static, Header, Footer
from rich.table import Table
from rich.text import Text
from textual.reactive import reactive
from textual.worker import Worker, WorkerState

class StockTab(Static):

    stocks_data = reactive({})
    loading = reactive(True)

    def on_mount(self) -> None:
        self.fetch_stock_data()
        self.set_interval(60, self.fetch_stock_data)

    def fetch_stock_data(self) -> None:
        self.loading = True
        self.run_worker(self._get_stock_data(), exclusive=True, group="stock_fetch")

    async def _get_stock_data(self) -> None:
        stocks = [
            "SLHN.SW", "ZURN.SW", "SREN.SW", "NOVN.SW",
            "HOLN.SW", "NESN.SW", "UHR.SW"
        ]
        new_data = {}

        for symbol in stocks:
            try:
                ticker = yf.Ticker(symbol)
                data = await self.app.run_in_thread(lambda s=symbol: ticker.history(period="1d", interval="1m"))

                if not data.empty:
                    open_price = data.iloc[0]['Open']
                    latest_price = data.iloc[-1]['Close']
                    change_percent = ((latest_price - open_price) / open_price) * 100
                    price_difference = latest_price - open_price

                    new_data[symbol] = {
                        "open": open_price,
                        "now": latest_price,
                        "change_percent": change_percent,
                        "price_difference": price_difference
                    }
                else:
                    new_data[symbol] = None
            except Exception as e:
                self.log(f"Error fetching data for {symbol}: {e}")
                new_data[symbol] = None

        self.stocks_data = new_data
        self.loading = False

    def watch_stocks_data(self, old_data: dict, new_data: dict) -> None:
        self.update()

    def render(self) -> Table | Text:
        if self.loading:
            return Text("Loading stock data...", style="italic blue", justify="center")

        table = Table(title="Portfolio Performance", expand=True)
        table.add_column("Symbol", style="bold")
        table.add_column("Open", justify="right")
        table.add_column("Now", justify="right")
        table.add_column("Change %", justify="right")
        table.add_column("Δ Price", justify="right")

        if not self.stocks_data:
            return Text("No stock data available. Please check your internet connection or stock symbols.", style="red", justify="center")

        for symbol, data in self.stocks_data.items():
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
                table.add_row(symbol, "-", "-", "No data", "No data")

        return table


class StockApp(App):
    BINDINGS = [("q", "quit", "Quit")]

    def compose(self) -> ComposeResult:
        yield Header()
        with TabbedContent():
            with TabPane("Portfolio", id="portfolio"):
                yield StockTab()
            with TabPane("Details", id="details"):
                yield Static("Details coming soon...")
            with TabPane("News", id="news"):
                yield Static("News coming soon...")
        yield Footer()

    def action_quit(self) -> None:
        self.exit()


if __name__ == "__main__":
    StockApp().run()