import csv
import glob
import os

output_file = "final_summary.csv"

files = glob.glob("data/trials/*.csv")

with open(output_file, "w", newline="") as out:
    writer = csv.writer(out)
    writer.writerow(["Generator", "Trial", "Test", "p-value", "Pass"])

    for filepath in files:
        filename = os.path.basename(filepath)

        if "mt_" in filename:
            gen = "C++ mt19937"
        elif "rd_" in filename:
            gen = "C++ random_device"
        elif "py_mt_" in filename:
            gen = "Python mt19937"
        elif "secure_" in filename:
            gen = "Python os.urandom"
        else:
            gen = "Unknown"

        trial = filename.split("_")[-1].replace(".csv", "")

        with open(filepath, "r") as f:
            reader = csv.reader(f)
            next(reader)  # skip header

            for row in reader:
                test, pval, passed = row
                writer.writerow([gen, trial, test, float(pval), passed])

print("Combined results written to final_summary.csv")
