import requests
import json
import time
from datetime import datetime


class CryptoTracker:
    """Class to track the price of a specific cryptocurrency."""

    def __init__(self, coin_id: str, display_name: str):
        self.coin_id = coin_id
        self.name = display_name
        self.BASE_URL = "https://api.coingecko.com/api/v3"

        self.price_usd = None
        self.price_idr = None
        self.market_cap = None
        self.volume_24h = None
        self.change_24h = None

        print(f"✅ Tracker initialized for: {self.name}")

    def fetch_price(self) -> bool:
        """Fetch real-time data from CoinGecko REST API."""
        print(f"🌐 Fetching data for {self.name}...")

        url = f"{self.BASE_URL}/simple/price"
        params = {
            "ids": self.coin_id,
            "vs_currencies": "usd,idr",
            "include_market_cap": "true",
            "include_24hr_vol": "true",
            "include_24hr_change": "true",
        }

        try:
            response = requests.get(url, params=params, timeout=15)
            response.raise_for_status()
            data = response.json()

            if self.coin_id not in data:
                print(f"❌ Coin '{self.coin_id}' not found.")
                return False

            coin_data = data[self.coin_id]
            self.price_usd = coin_data.get("usd", 0)
            self.price_idr = coin_data.get("idr", 0)
            self.market_cap = coin_data.get("usd_market_cap", 0)
            self.volume_24h = coin_data.get("usd_24h_vol", 0)
            self.change_24h = coin_data.get("usd_24h_change", 0)

            return True

        except Exception as e:
            print(f"❌ Error fetching data: {e}")
            return False

    def display_info(self) -> None:
        """Print formatted coin information to the console."""
        if self.price_usd is None:
            print(f"⚠️ Data for {self.name} is not available yet.")
            return

        trend = "📈" if self.change_24h >= 0 else "📉"
        timestamp = datetime.now().strftime("%d %B %Y %H:%M")

        print("\n" + "=" * 45)
        print(f"  💰  {self.name.upper()}")
        print(f"  🕐  {timestamp}")
        print("=" * 45)
        print(f"  Price (USD)   : $ {self.price_usd:,.2f}")
        print(f"  Price (IDR)   : Rp {self.price_idr:,.0f}")
        print(f"  Market Cap    : $ {self.market_cap:,.0f}")
        print(f"  24h Change    : {trend} {self.change_24h:.2f}%")
        print("=" * 45)

    def save_report(self) -> None:
        """Save the current data to a JSON file."""
        if self.price_usd is None: return

        date_str = datetime.now().strftime("%Y%m%d")
        filename = f"report_Crypto_{self.coin_id}_{date_str}.json"
        report = {
            "coin": self.name,
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "price_usd": self.price_usd,
            "change_24h": self.change_24h
        }

        with open(filename, "w") as f:
            json.dump(report, f, indent=2)
        print(f"💾 Report saved: {filename}")

    def check_volatility(self, threshold: float = 5.0) -> None:
        """Check if the coin is experiencing high volatility."""
        if self.change_24h is None:
            print(f"⚠️  Change data for {self.name} is unavailable.")
            return

        current_volatility = abs(self.change_24h)

        print(f"\n🔍 [Monitoring System: {self.name}]")

        if current_volatility >= threshold:
            status = "SKYROCKETING 🚀" if self.change_24h > 0 else "PLUMMETING 📉"
            print(f"🚨 ALERT: {self.name} is {status}!")
            print(f"📊 Change: {self.change_24h:+.2f}% (Threshold: {threshold}%)")
            print(f"💡 Advice: Check the latest news regarding {self.name}!")
        else:
            print(f"✅ Market condition for {self.name} is stable.")
            print(f"📊 Change: {self.change_24h:+.2f}% (Below {threshold}% threshold)")


# --- Global Helper Functions ---

def compare_coins(coin_list: list) -> None:
    valid_coins = [k for k in coin_list if k.change_24h is not None]
    if not valid_coins: return

    print("\n" + "=" * 50)
    print("  📊 CRYPTO PRICE COMPARISON")
    print("=" * 50)
    print(f"  {'Name':<15} {'Price USD':>12} {'24h %':>8}")
    print("-" * 50)

    for k in valid_coins:
        icon = "▲" if k.change_24h >= 0 else "▼"
        print(f"  {k.name:<15} ${k.price_usd:>11,.2f}  {icon}{abs(k.change_24h):.2f}%")

    top_performer = max(valid_coins, key=lambda k: k.change_24h)
    worst_performer = min(valid_coins, key=lambda k: k.change_24h)
    print("-" * 50)
    print(f"🏆 Best Performer: {top_performer.name} ({top_performer.change_24h:+.2f}%)")
    print(f"📉 Weakest: {worst_performer.name} ({worst_performer.change_24h:+.2f}%)")
    print("=" * 50)


def market_summary(coin_list: list) -> None:
    valid_coins = [k for k in coin_list if k.price_usd is not None]
    if not valid_coins: return

    total_mc = sum(k.market_cap for k in valid_coins)
    avg_change = sum(k.change_24h for k in valid_coins) / len(valid_coins)

    print("\n" + "=" * 30)
    print("      GLOBAL MARKET SUMMARY")
    print("-" * 30)
    print(f"Coins Monitored  : {len(valid_coins)}")
    print(f"Avg 24h Change   : {avg_change:+.2f}%")
    print(f"Total Market Cap : $ {total_mc / 1_000_000_000_000:.2f} T")
    print("=" * 30)
