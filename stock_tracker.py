import yfinance as yf
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import pandas as pd
from datetime import datetime
import csv
import os
from datetime import timezone

TICKERS = ["BKSY", "IONQ", "QNT", "GDYN"]
LOG_FILE = "stocks.csv"
CHART_FILE = "stock_chart.png"
COLORS = {"BKSY": "#4C9BE8", "IONQ": "#F4A261", "QNT": "#2EC4B6", "GDYN": "#E84855"}


def get_prices():
    timestamp = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")
    results = {}
    for ticker in TICKERS:
        try:
            info = yf.Ticker(ticker).fast_info
            price = round(info.last_price, 2)
            prev_close = round(info.previous_close, 2)
            change = round(price - prev_close, 2)
            pct = round((change / prev_close) * 100, 2)
            results[ticker] = {"price": price, "prev_close": prev_close, "change": change, "pct": pct}
        except Exception as e:
            print(f"Error fetching {ticker}: {e}")
            results[ticker] = None
    return timestamp, results


def append_log(timestamp, results):
    file_exists = os.path.exists(LOG_FILE)
    with open(LOG_FILE, "a", newline="") as f:
        writer = csv.writer(f)
        if not file_exists:
            writer.writerow(["timestamp", "ticker", "price", "prev_close", "change", "pct_change"])
        for ticker, data in results.items():
            if data:
                writer.writerow([timestamp, ticker, data["price"], data["prev_close"], data["change"], data["pct"]])


def build_chart():
    if not os.path.exists(LOG_FILE):
        return

    df = pd.read_csv(LOG_FILE)
    df["timestamp"] = pd.to_datetime(df["timestamp"])

    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(13, 8))
    fig.suptitle("Quantum and AI Stocks", fontsize=15, fontweight="bold", y=0.98)

    for ticker in TICKERS:
        tdata = df[df["ticker"] == ticker].sort_values("timestamp")
        if tdata.empty:
            continue
        color = COLORS.get(ticker, "gray")
        ax1.plot(tdata["timestamp"], tdata["price"], marker="o", markersize=4,
                 linewidth=1.5, label=ticker, color=color)
        ax2.plot(tdata["timestamp"], tdata["pct_change"], marker="o", markersize=4,
                 linewidth=1.5, label=ticker, color=color)

    ax1.set_ylabel("Price (USD)")
    ax1.set_title("Price", fontsize=11)
    ax1.legend()
    ax1.grid(True, alpha=0.3)
    ax1.set_facecolor("#f8f9fa")

    ax2.set_ylabel("Change (%)")
    ax2.set_title("Daily Change (%)", fontsize=11)
    ax2.axhline(0, color="gray", linewidth=0.8, linestyle="--")
    ax2.legend()
    ax2.grid(True, alpha=0.3)
    ax2.set_facecolor("#f8f9fa")

    for ax in [ax1, ax2]:
        ax.xaxis.set_major_formatter(mdates.DateFormatter("%m-%d"))
        ax.xaxis.set_major_locator(mdates.WeekdayLocator(interval=1))

    fig.autofmt_xdate()
    fig.patch.set_facecolor("#ffffff")
    plt.tight_layout()
    plt.savefig(CHART_FILE, dpi=150, bbox_inches="tight")
    print(f"Chart saved to {CHART_FILE}")


if __name__ == "__main__":
    timestamp, results = get_prices()
    print(f"\n{timestamp}")
    for ticker, data in results.items():
        if data:
            sign = "+" if data["change"] >= 0 else ""
            print(f"  {ticker}: ${data['price']} ({sign}{data['change']} / {sign}{data['pct']}%)")
        else:
            print(f"  {ticker}: fetch failed")
    append_log(timestamp, results)
    build_chart()
