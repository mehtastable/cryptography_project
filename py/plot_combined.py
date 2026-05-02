import pandas as pd
import matplotlib.pyplot as plt

# Load data
df = pd.read_csv("results/final_summary.csv")
df["p-value"] = df["p-value"].astype(float)

tests = df["Test"].unique()
generators = df["Generator"].unique()

# Create subplot grid (1 row per test)
fig, axes = plt.subplots(len(tests), 1, figsize=(10, 12), sharex=True)

if len(tests) == 1:
    axes = [axes]  # ensure iterable

for ax, test in zip(axes, tests):
    subset = df[df["Test"] == test]

    data_to_plot = [
        subset[subset["Generator"] == gen]["p-value"].values
        for gen in generators
    ]

    ax.boxplot(data_to_plot, labels=generators)
    ax.set_title(f"P-value Distribution: {test}")
    ax.set_ylim(0, 1)
    ax.set_ylabel("p-value")

plt.xticks(rotation=20)
plt.tight_layout()

plt.savefig("combined_boxplots.png", dpi=300)
plt.show()
