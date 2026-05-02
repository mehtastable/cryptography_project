import pandas as pd
import glob
import os
import matplotlib.pyplot as plt
import numpy as np
from scipy.special import gammaincc
import sys

### uniformity test function
def uniformity_test(p_values, bins=10):
    p_values = np.array(p_values)
    counts, _ = np.histogram(p_values, bins=bins, range=(0.0, 1.0))
    n = len(p_values)
    expected = n / bins
    chi_sq = np.sum((counts - expected) ** 2 / expected)
    p_uniform = gammaincc((bins - 1) / 2.0, chi_sq / 2.0)
    return chi_sq, p_uniform


### proportion test function
def proportion_test(p_values, alpha=0.01):
    p_values = np.array(p_values)
    n = len(p_values)
    passes = np.sum(p_values > alpha)
    prop = passes / n
    p_hat = 1 - alpha
    std = np.sqrt((p_hat * (1 - p_hat)) / n)
    lower = p_hat - 3 * std
    upper = p_hat + 3 * std
    return prop, lower, upper, (lower <= prop <= upper)

### main
def main(base_dir, trials):
    trials_dir = os.path.join(base_dir, f"data_{trials}", f"trials_{trials}")
    res_dir = os.path.join(base_dir, f"results_{trials}")
    os.makedirs(res_dir, exist_ok=True)
    files = sorted(glob.glob(os.path.join(trials_dir, "*.csv")))
    rows = []
    ### load data
    for f in files:
        name = os.path.basename(f)
        if name.startswith("cpp_mt_"):
            gen = "C++ mt19937"
        elif name.startswith("cpp_rd_"):
            gen = "C++ random_device"
        elif name.startswith("py_mt_"):
            gen = "Python mt19937"
        elif name.startswith("py_os_"):
            gen = "Python os.urandom"
        else:
            continue
        df_file = pd.read_csv(f)
        for _, r in df_file.iterrows():
            rows.append([gen, r["Test"], float(r["p-value"])])
    df = pd.DataFrame(rows, columns=["Generator", "Test", "p-value"])
    
    ### write summary stats
    summary = df.groupby(["Generator", "Test"]).agg(
        mean_p=("p-value", "mean"),
        std_p=("p-value", "std")
    ).reset_index()
    summary.to_csv(os.path.join(res_dir, f"summary_stats_{trials}.csv"), index=False)

    ### write uniformity test
    uniform_rows = []
    for gen in df["Generator"].unique():
        for test in df["Test"].unique():
            subset = df[(df["Generator"] == gen) & (df["Test"] == test)]
            pvals = subset["p-value"].values
            if len(pvals) < 10:
                continue
            chi_sq, p_uniform = uniformity_test(pvals)
            uniform_rows.append([gen, test, chi_sq, p_uniform])
    uniform_df = pd.DataFrame(
        uniform_rows,
        columns=["Generator", "Test", "Chi-square", "Uniformity p-value"]
    )
    uniform_df.to_csv(os.path.join(res_dir, f"uniformity_test_{trials}.csv"), index=False)

    ### write proportion passing test
    prop_rows = []
    for gen in df["Generator"].unique():
        for test in df["Test"].unique():
            subset = df[(df["Generator"] == gen) & (df["Test"] == test)]
            pvals = subset["p-value"].values
            if len(pvals) == 0:
                continue
            prop, lower, upper, passed = proportion_test(pvals)
            prop_rows.append([gen, test, prop, lower, upper, passed])
    prop_df = pd.DataFrame(
        prop_rows,
        columns=["Generator", "Test", "Proportion", "Lower", "Upper", "Pass"]
    )
    prop_df.to_csv(os.path.join(res_dir, f"proportion_test_{trials}.csv"), index=False)

    ### text report file
    with open(os.path.join(res_dir, f"summary_report_{trials}.txt"), "w") as f:
        f.write("RANDOMNESS EXPERIMENT SUMMARY\n\n")
        ### summary of stats
        for gen in summary["Generator"].unique():
            f.write(f"Generator: {gen}\n")
            sub = summary[summary["Generator"] == gen]
            for _, row in sub.iterrows():
                f.write(f"{row['Test']}\n")
                f.write(f"  Mean p-value: {row['mean_p']:.4f}\n")
                f.write(f"  Std dev     : {row['std_p']:.4f}\n\n")

        ### uniformity test
        f.write("\n\nUNIFORMITY TEST (NIST)\n")
        for _, row in uniform_df.iterrows():
            f.write(f"{row['Generator']} - {row['Test']}\n")
            f.write(f"  Chi-square: {row['Chi-square']:.4f}\n")
            f.write(f"  p-value   : {row['Uniformity p-value']:.4f}\n")
            if row["Uniformity p-value"] < 0.0001:
                f.write("  Result    : FAIL (non-uniform)\n\n")
            else:
                f.write("  Result    : PASS\n\n")

        ### proportion passing
        f.write("\n\nPROPORTION OF PASSING (NIST)\n")
        for _, row in prop_df.iterrows():
            f.write(f"{row['Generator']} - {row['Test']}\n")
            f.write(f"  Observed proportion: {row['Proportion']:.4f}\n")
            f.write(f"  Expected range    : [{row['Lower']:.4f}, {row['Upper']:.4f}]\n")
            if row["Pass"]:
                f.write("  Result            : PASS\n\n")
            else:
                f.write("  Result            : FAIL\n\n")

    ### combined box plots
    tests = df["Test"].unique()
    gens = df["Generator"].unique()
    fig, axes = plt.subplots(len(tests), 1, figsize=(10, 12), sharex=True)
    if len(tests) == 1:
        axes = [axes]
    for ax, test in zip(axes, tests):
        subset = df[df["Test"] == test]
        data = [
            subset[subset["Generator"] == g]["p-value"]
            for g in gens
        ]
        ax.boxplot(data, labels=gens)
        ax.set_title(test)
        ax.set_ylim(0, 1)
        ax.set_ylabel("p-value")
    plt.xticks(rotation=20)
    plt.tight_layout()
    plt.savefig(os.path.join(res_dir, f"combined_boxplots_{trials}.png"), dpi=300)
    plt.close()
    print("Summary + plots complete.")  
    gens = df["Generator"].unique()
    bins = np.linspace(0, 1, 11)
    fig, axes = plt.subplots(len(gens), 1, figsize=(10, 8), sharex=True)

    if len(gens) == 1:
        axes = [axes]
    for ax, gen in zip(axes, gens):
        subset = df[df["Generator"] == gen]["p-value"]
        ax.hist(
            subset,
            bins=bins,
            edgecolor="black"
        )
        ax.set_title(f"{gen}")
        ax.set_ylabel("Count")
        ax.set_ylim(0, None)
    axes[-1].set_xlabel("p-value (0 to 1)")
    plt.tight_layout()
    plt.savefig(os.path.join(res_dir, f"uniformity_histogram_by_generator_{trials}.png"), dpi=300)
    plt.close()

### program entry
if __name__ == "__main__":
    base_dir = sys.argv[1]
    trials = int(sys.argv[2])
    main(base_dir, trials)
