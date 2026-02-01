from __future__ import annotations

import pandas as pd
import seaborn as sns
from matplotlib import pyplot as plt
from matplotlib.axes import Axes
from matplotlib.figure import Figure

# 1) Load data
df: pd.DataFrame = pd.read_csv("data/data.csv", parse_dates=["date"])

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
scatter_fig, scatter_ax = plt.subplots(figsize=(6, 5))
scatter_fig = cast(Figure, scatter_fig)
scatter_ax = cast(Axes, scatter_ax)
sns.scatterplot(
    data=df,
    x="temp_c",
    y="humidity",
    hue="is_weekend",
    palette=["gray", "orange"],
    ax=scatter_ax,
)
sns.regplot(
    data=df, x="temp_c", y="humidity", scatter=False, color="black", ax=scatter_ax
)
plt.title("Temp vs Humidity")
plt.show()

# 6) Brief notes
print("Observations: ...")
