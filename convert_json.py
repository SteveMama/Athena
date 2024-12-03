import pandas as pd
import json
import os

# Input directory
input_directory = "Amsterdam_dataset"

# Output directory
output_directory = "output_json"
os.makedirs(output_directory, exist_ok=True)

# List of specified admission IDs
specified_admission_ids = [2642, 5791, 1646, 6867, 3442, 2769, 1876, 9061, 8641, 1817]

# Function to read, filter, and convert DataFrame to JSON
def process_dataset(file_name, dataset_name, admission_id_column, specified_ids, output_directory):
    # Read the CSV file
    df = pd.read_csv(os.path.join(input_directory, file_name))
    # Filter rows based on specified admission IDs
    filtered_df = df[df[admission_id_column].isin(specified_ids)]
    # Convert to JSON
    json_entries = []
    for _, row in filtered_df.iterrows():
        entry = row.to_dict()
        entry["dataset"] = dataset_name
        json_entries.append(entry)
    json_filename = os.path.join(output_directory, f"{dataset_name.lower().replace(' ', '_')}_data.json")
    with open(json_filename, 'w') as json_file:
        json.dump(json_entries, json_file, indent=4)
    return json_entries

# Process each dataset
admissions_json = process_dataset(
    file_name="Admissions_Dataset.csv",
    dataset_name="Admissions Dataset",
    admission_id_column="admissionid",
    specified_ids=specified_admission_ids,
    output_directory=output_directory,
)

medication_json = process_dataset(
    file_name="Medication_Dataset.csv",
    dataset_name="Medication Dataset",
    admission_id_column="admissionid",
    specified_ids=specified_admission_ids,
    output_directory=output_directory,
)

results_json = process_dataset(
    file_name="Results_Dataset.csv",
    dataset_name="Results Dataset",
    admission_id_column="admissionid",
    specified_ids=specified_admission_ids,
    output_directory=output_directory,
)

process_items_json = process_dataset(
    file_name="Process_Items_Dataset.csv",
    dataset_name="Process Items Dataset",
    admission_id_column="admissionid",
    specified_ids=specified_admission_ids,
    output_directory=output_directory,
)

procedure_order_items_json = process_dataset(
    file_name="Procedure_Order_Items_Dataset.csv",
    dataset_name="Procedure Order Items Dataset",
    admission_id_column="admissionid",
    specified_ids=specified_admission_ids,
    output_directory=output_directory,
)

print("Filtered CSV to JSON conversion completed successfully.")
