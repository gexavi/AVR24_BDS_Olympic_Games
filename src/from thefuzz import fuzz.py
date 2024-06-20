
from thefuzz import fuzz
import pandas as pd


df1 = pd.read_csv("E:/Json/final/WA_temps_final.csv")
df2 = pd.read_csv("E:/Json/final/wr_progression_1983plus_temps.csv", encoding='latin')

#fuzz.ratio(df1.Name, df2.Name)
for i in df1.Name:
    for j in df2.Name:
        #process.extract(i, j)
        if fuzz.ratio(i, j) > 80:
            print(i,";", j)
