import pandas as pd

df = pd.read_csv("final_summary.csv")

summary = df.groupby(["Generator", "Test"])["p-value"].agg(["mean", "std", "min", "max"])

summary.to_csv("summary_stats.csv")

print(summary)
