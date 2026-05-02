import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv("final_summary.csv")

# Ensure numeric
df["p-value"] = df["p-value"].astype(float)

tests = df["Test"].unique()

for test in tests:
    subset = df[df["Test"] == test]

    plt.figure()
    subset.boxplot(column="p-value", by="Generator")

    plt.title(f"P-value Distribution: {test}")
    plt.suptitle("")  # remove default title
    plt.ylim(0, 1)
    plt.xticks(rotation=20)

    filename = f"boxplot_{test.replace(' ', '_')}.png"
    plt.savefig(filename)
    plt.close()

print("Boxplots saved.")
