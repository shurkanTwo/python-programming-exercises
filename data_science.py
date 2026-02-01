from __future__ import annotations

import pandas as pd
import seaborn as sns
from matplotlib import pyplot as plt
from matplotlib.axes import Axes
from matplotlib.figure import Figure

# 1) Load data
df: pd.DataFrame = pd.read_csv("data.csv", parse_dates=["date"])

# If mocking data instead of reading the CSV, replace the block below with real numbers.
# mock_data: Dict[str, Any] = {
#     "date": pd.date_range("2024-01-01", periods=30, freq="D"),
#     "temp_c": [4.2, 4.8, 5.1, 5.6, 6.0, 6.3, 6.8, 7.0, 7.4, 7.9, 8.1, 8.5, 8.9, 9.2, 9.5, 9.8, 10.1, 10.4, 10.8, 11.0, 11.3, 11.7, 12.0, 12.4, 12.8, 13.1, 13.5, 13.9, 14.2, 14.6],
#     "humidity": [82, 80, 78, 76, 74, 79, 81, 77, 75, 72, 70, 73, 78, 80, 76, 74, 71, 69, 72, 75, 77, 74, 71, 69, 67, 70, 73, 75, 72, 70],
# }
# df = pd.DataFrame(mock_data)

# 2) Clean / prep
df["date"] = pd.to_datetime(df["date"])
df["weekday"] = df["date"].dt.day_name()
df["is_weekend"] = df["date"].dt.weekday >= 5
df = df.dropna()  # or fillna

# 3) Basic stats
stats: pd.DataFrame = df[["temp_c", "humidity"]].describe()
corr_value: float = float(df["temp_c"].corr(df["humidity"]))
print(stats)
print("Correlation:", corr_value)

# 4) Line plot over time
sns.set_theme()
fig: Figure
ax1: Axes
fig, ax1 = plt.subplots(figsize=(10, 4))
sns.lineplot(data=df, x="date", y="temp_c", ax=ax1, label="Temp (C)", color="tomato")
ax2: Axes = ax1.twinx()
sns.lineplot(
    data=df, x="date", y="humidity", ax=ax2, label="Humidity", color="royalblue"
)
ax1.set_ylabel("Temp (C)")
ax2.set_ylabel("Humidity (%)")
plt.title("Daily Temp vs Humidity")
fig.tight_layout()
plt.show()

# 5) Scatter with hue by weekend (and trendline)
scatter_fig: Figure = plt.figure(figsize=(6, 5))
scatter_ax: Axes = sns.scatterplot(
    data=df, x="temp_c", y="humidity", hue="is_weekend", palette=["gray", "orange"]
)
sns.regplot(
    data=df, x="temp_c", y="humidity", scatter=False, color="black", ax=scatter_ax
)
plt.title("Temp vs Humidity")
plt.show()

# 6) Brief notes
print("Observations: ...")
