import pandas as pd
import json
import os

input_directory = "Amsterdam_dataset"
admissions_df = pd.read_csv(os.path.join(input_directory, "Admissions_Dataset.csv"), nrows=10)
medication_df = pd.read_csv(os.path.join(input_directory, "Medication_Dataset.csv"), nrows=10)
results_df = pd.read_csv(os.path.join(input_directory, "Results_Dataset.csv"), nrows=10)
process_items_df = pd.read_csv(os.path.join(input_directory, "Process_Items_Dataset.csv"), nrows=10)
procedure_order_items_df = pd.read_csv(os.path.join(input_directory, "Procedure_Order_Items_Dataset.csv"), nrows=10)

def dataframe_to_json(df, dataset_name, output_directory):
    json_entries = []
    for _, row in df.iterrows():
        entry = row.to_dict()
        entry["dataset"] = dataset_name
        json_entries.append(entry)
    json_filename = os.path.join(output_directory, f"{dataset_name.lower().replace(' ', '_')}_data.json")
    with open(json_filename, 'w') as json_file:
        json.dump(json_entries, json_file, indent=4)
    return json_entries

output_directory = "output_json"
os.makedirs(output_directory, exist_ok=True)

admissions_json = dataframe_to_json(admissions_df, "Admissions Dataset", output_directory)
medication_json = dataframe_to_json(medication_df, "Medication Dataset", output_directory)
results_json = dataframe_to_json(results_df, "Results Dataset", output_directory)
process_items_json = dataframe_to_json(process_items_df, "Process Items Dataset", output_directory)
procedure_order_items_json = dataframe_to_json(procedure_order_items_df, "Procedure Order Items Dataset", output_directory)

print("CSV to JSON conversion completed successfully.")