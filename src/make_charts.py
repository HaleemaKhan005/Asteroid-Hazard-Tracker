from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

base = Path(__file__).resolve().parent.parent
df = pd.read_csv(base / "data" / "asteroids.csv")

charts_folder = base / "charts"
charts_folder.mkdir(exist_ok=True)

sns.set_theme(style="whitegrid")

# Chart 1: how many hazardous vs not
plt.figure(figsize=(6, 4))
sns.countplot(data=df, x="hazardous")
plt.title("Hazardous vs Not Hazardous Asteroids")
plt.xlabel("Potentially hazardous?")
plt.ylabel("Number of asteroids")
plt.savefig(charts_folder / "chart1_hazardous_count.png", dpi=150, bbox_inches="tight")
plt.show()

# Chart 2: size vs miss distance
plt.figure(figsize=(8, 5))
sns.scatterplot(
    data=df,
    x="diameter_max_m",
    y="miss_distance_km",
    hue="hazardous",
    alpha=0.7,
)
plt.xscale("log")
plt.title("Asteroid Size vs Miss Distance")
plt.xlabel("Maximum diameter (meters, log scale)")
plt.ylabel("Miss distance (km)")
plt.savefig(charts_folder / "chart2_size_vs_distance.png", dpi=150, bbox_inches="tight")
plt.show()

# Chart 3: size comparison by group
plt.figure(figsize=(6, 5))
sns.boxplot(data=df, x="hazardous", y="diameter_max_m")
plt.yscale("log")
plt.title("Asteroid Size: Hazardous vs Not Hazardous")
plt.xlabel("Potentially hazardous?")
plt.ylabel("Maximum diameter (meters, log scale)")
plt.savefig(charts_folder / "chart3_size_by_group.png", dpi=150, bbox_inches="tight")
plt.show()

# Chart 4: average speed by group
avg_speed = df.groupby("hazardous")["velocity_kmps"].mean().reset_index()

plt.figure(figsize=(6, 4))
ax = sns.barplot(data=avg_speed, x="hazardous", y="velocity_kmps")
ax.bar_label(ax.containers[0], fmt="%.1f")
plt.title("Average Asteroid Speed: Hazardous vs Not Hazardous")
plt.xlabel("Potentially hazardous?")
plt.ylabel("Average speed (km per second)")
plt.savefig(charts_folder / "chart4_speed_by_group.png", dpi=150, bbox_inches="tight")
plt.show()

# Chart 5: average miss distance by group
avg_dist = (
    df.groupby("hazardous")["miss_distance_km"]
    .mean()
    .div(1_000_000)
    .reset_index(name="avg_distance_million_km")
)

plt.figure(figsize=(6, 4))
ax = sns.barplot(data=avg_dist, x="hazardous", y="avg_distance_million_km")
ax.bar_label(ax.containers[0], fmt="%.1f")
plt.title("Average Miss Distance: Hazardous vs Not Hazardous")
plt.xlabel("Potentially hazardous?")
plt.ylabel("Average miss distance (million km)")
plt.savefig(charts_folder / "chart5_distance_by_group.png", dpi=150, bbox_inches="tight")
plt.show()