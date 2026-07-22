import re
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from datetime import datetime

dates, west, east = [], [], []

with open("ping.log") as f:
    for line in f:
        line = line.strip()
        if not line:
            continue
        m = re.match(r"(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}) \| WEST=(\d+\.\d+)ms \| EAST=(\d+\.\d+)ms", line)
        if m:
            dates.append(datetime.strptime(m.group(1), "%Y-%m-%d %H:%M:%S"))
            west.append(float(m.group(2)))
            east.append(float(m.group(3)))

fig, ax = plt.subplots(figsize=(12, 5))
ax.plot(dates, west, marker="o", markersize=4, linewidth=1.5, label="WEST (8.8.8.8)", color="#4C9BE8")
ax.plot(dates, east, marker="o", markersize=4, linewidth=1.5, label="EAST (1.1.1.1)", color="#F4A261")

ax.set_title("Network Latency", fontsize=14, fontweight="bold", pad=12)
ax.set_ylabel("Latency (ms)")
ax.xaxis.set_major_formatter(mdates.DateFormatter("%m-%d"))
ax.xaxis.set_major_locator(mdates.WeekdayLocator(interval=1))
fig.autofmt_xdate()
ax.legend()
ax.grid(True, alpha=0.3)
ax.set_facecolor("#f8f9fa")
fig.patch.set_facecolor("#ffffff")
plt.tight_layout()
plt.savefig("ping_chart.png", dpi=150, bbox_inches="tight")
print("Chart saved to ping_chart.png")
