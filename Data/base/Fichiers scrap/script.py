import pandas as pd
df = pd.read_csv("1896_summer_men.csv", sep = ";")
df.isna().sum()