import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


admissions_df = pd.read_csv("Amsterdam_dataset/Admissions_Dataset.csv")
medication_df = pd.read_csv("Amsterdam_dataset/Medication_Dataset.csv")
results_df = pd.read_csv("Amsterdam_dataset/Results_Dataset.csv")
process_items_df = pd.read_csv("Amsterdam_dataset/Process_Items_Dataset.csv")
procedure_order_items_df = pd.read_csv("Amsterdam_dataset/Procedure_Order_Items_Dataset.csv")


def dataset_overview(df, name):
    print(f"Dataset: {name}")
    print(f"Shape: {df.shape}")
    print("Columns and Data Types:")
    print(df.dtypes)
    print("\nMissing Values:")
    print(df.isnull().sum())
    print("\nBasic Statistics:")
    print(df.describe(include='all'))
    print("-" * 40)


datasets = {
    "Admissions Dataset": admissions_df,
    "Medication Dataset": medication_df,
    "Results Dataset": results_df,
    "Process Items Dataset": process_items_df,
    "Procedure Order Items Dataset": procedure_order_items_df,
}

for name, df in datasets.items():
    dataset_overview(df, name)

# Visualization examples
def plot_distributions(df, column, title):
    if column in df.columns:
        plt.figure(figsize=(10, 6))
        sns.histplot(df[column].dropna(), kde=True, bins=20)
        plt.title(f"{title} Distribution")
        plt.xlabel(column)
        plt.ylabel("Frequency")
        plt.show()

# Admissions Analysis
plot_distributions(admissions_df, "lengthofstay", "Length of Stay")
plot_distributions(admissions_df, "agegroup", "Age Group")

# Medication Analysis
plot_distributions(medication_df, "rate", "Medication Infusion Rate")

# Process Items Analysis
plot_distributions(process_items_df, "duration", "Process Duration")

# Procedure Order Items Analysis
procedure_order_items_df["registeredby"].value_counts().plot(kind="bar", figsize=(8, 5))
plt.title("Procedure Orders by User Group")
plt.xlabel("User Group")
plt.ylabel("Count")
plt.show()
