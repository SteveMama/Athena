import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


admissions_df = pd.read_csv("Amsterdam_dataset/Admissions_Dataset.csv")
medication_df = pd.read_csv("Amsterdam_dataset/Medication_Dataset.csv")
results_df = pd.read_csv("Amsterdam_dataset/Results_Dataset.csv")
process_items_df = pd.read_csv("Amsterdam_dataset/Process_Items_Dataset.csv")
procedure_order_items_df = pd.read_csv("Amsterdam_dataset/Procedure_Order_Items_Dataset.csv")

admissions_df['admittedat'] = pd.to_datetime(admissions_df['admittedat'], errors='coerce')
admissions_df['dischargedat'] = pd.to_datetime(admissions_df['dischargedat'], errors='coerce')
medication_df['start'] = pd.to_datetime(medication_df['start'], errors='coerce')
medication_df['stop'] = pd.to_datetime(medication_df['stop'], errors='coerce')
process_items_df['start'] = pd.to_datetime(process_items_df['start'], errors='coerce')
process_items_df['stop'] = pd.to_datetime(process_items_df['stop'], errors='coerce')
procedure_order_items_df['registeredat'] = pd.to_datetime(procedure_order_items_df['registeredat'], errors='coerce')

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

# Admissions Trend Analysis
def plot_admissions_trend(df):
    plt.figure(figsize=(12, 6))
    admissions_per_year = df['admissionyeargroup'].value_counts().sort_index()
    sns.lineplot(x=admissions_per_year.index, y=admissions_per_year.values, marker="o")
    plt.title("Number of Admissions per Year")
    plt.xlabel("Year")
    plt.ylabel("Number of Admissions")
    plt.xticks(rotation=45)
    plt.grid()
    plt.show()

#plot_admissions_trend(admissions_df)

# Length of Stay Trend Analysis
def plot_length_of_stay_trend(df):
    plt.figure(figsize=(12, 6))
    df['admission_month'] = df['admittedat'].dt.month
    average_length_of_stay = df.groupby('admission_month')['lengthofstay'].mean()
    sns.lineplot(x=average_length_of_stay.index, y=average_length_of_stay.values, marker="o")
    plt.title("Average Length of Stay per Month")
    plt.xlabel("Month")
    plt.ylabel("Average Length of Stay (hours)")
    plt.xticks(range(1, 13))
    plt.grid()
    plt.show()

#plot_length_of_stay_trend(admissions_df)

# Gender Distribution Over Time
def plot_gender_distribution_trend(df):
    plt.figure(figsize=(12, 6))
    admissions_per_gender = df.groupby([df['admittedat'].dt.year, 'gender']).size().unstack()
    admissions_per_gender.plot(kind='bar', stacked=True, figsize=(10, 6))
    plt.title("Gender Distribution of Admissions Over Years")
    plt.xlabel("Year")
    plt.ylabel("Number of Admissions")
    plt.xticks(rotation=45)
    plt.grid()
    plt.show()

#plot_gender_distribution_trend(admissions_df)

# Medication Infusion Rate Trend Analysis
def plot_medication_rate_trend(df):
    plt.figure(figsize=(12, 6))
    df['start_month'] = df['start'].dt.month
    average_medication_rate = df.groupby('start_month')['rate'].mean()
    sns.lineplot(x=average_medication_rate.index, y=average_medication_rate.values, marker="o")
    plt.title("Average Medication Infusion Rate per Month")
    plt.xlabel("Month")
    plt.ylabel("Infusion Rate (ml/hour or equivalent)")
    plt.xticks(range(1, 13))
    plt.grid()
    plt.show()

#plot_medication_rate_trend(medication_df)

# Procedure Orders Trend Analysis
def plot_procedure_orders_trend(df):
    plt.figure(figsize=(12, 6))
    procedure_per_month = df['registeredat'].dt.month.value_counts().sort_index()
    sns.lineplot(x=procedure_per_month.index, y=procedure_per_month.values, marker="o")
    plt.title("Number of Procedures Registered per Month")
    plt.xlabel("Month")
    plt.ylabel("Number of Procedures")
    plt.xticks(range(1, 13))
    plt.grid()
    plt.show()

#plot_procedure_orders_trend(procedure_order_items_df)

# Process Item Trends Analysis
def plot_process_items_trend(df):
    plt.figure(figsize=(12, 6))
    df['start_month'] = df['start'].dt.month
    process_per_month = df['start_month'].value_counts().sort_index()
    sns.lineplot(x=process_per_month.index, y=process_per_month.values, marker="o")
    plt.title("Number of Process Items Introduced per Month")
    plt.xlabel("Month")
    plt.ylabel("Number of Processes")
    plt.xticks(range(1, 13))
    plt.grid()
    plt.show()

#plot_process_items_trend(process_items_df)