from pathlib import Path

import pandas as pd

path = Path(__file__).resolve().parent.parent / "data" / "asteroids.csv"
df = pd.read_csv(path)

pd.set_option("display.max_columns", None)
pd.set_option("display.width", 200)

print("Shape:", df.shape)
print()
print("Missing values per column:")
print(df.isnull().sum())
print()
print("Data types:")
print(df.dtypes)
print()
print("Summary statistics:")
print(df.describe())
print()
print("Hazardous counts:")
print(df["hazardous"].value_counts())