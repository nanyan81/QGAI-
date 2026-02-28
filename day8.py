import pandas as pd
import numpy as np

dates = pd.date_range("20130101", periods=6)


df = pd.DataFrame(np.random.randn(6, 4), index=dates, columns=list("ABCD"))

print(df)

df2=df.copy()
df2["D"] = ["1","2","3","4","5","6"]
print(df2)
df3 = df2[df2.loc[:,"D"].isin(["2","4"])]
print(df3)

df4 = pd.read_csv("housing.csv")
print(df4)
