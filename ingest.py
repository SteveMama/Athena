import os

import pandas as pd
import json
from sentence_transformers import SentenceTransformer

from pinecone import Pinecone, ServerlessSpec

from dotenv import load_dotenv
load_dotenv()


admissions_df = pd.read_csv("Amsterdam_dataset/Admissions_Dataset.csv")
medication_df = pd.read_csv("Amsterdam_dataset/Medication_Dataset.csv")
results_df = pd.read_csv("Amsterdam_dataset/Results_Dataset.csv")
process_items_df = pd.read_csv("Amsterdam_dataset/Process_Items_Dataset.csv")
procedure_order_items_df = pd.read_csv("Amsterdam_dataset/Procedure_Order_Items_Dataset.csv")


def dataframe_to_json(df, dataset_name):
    json_entries = []
    for _, row in df.iterrows():
        entry = row.to_dict()
        entry["dataset"] = dataset_name
        json_entries.append(json.dumps(entry))
    return json_entries


admissions_json = dataframe_to_json(admissions_df, "Admissions Dataset")
medication_json = dataframe_to_json(medication_df, "Medication Dataset")
results_json = dataframe_to_json(results_df, "Results Dataset")
process_items_json = dataframe_to_json(process_items_df, "Process Items Dataset")
procedure_order_items_json = dataframe_to_json(procedure_order_items_df, "Procedure Order Items Dataset")

def dataframe_to_json(df, dataset_name):
    json_entries = []
    for _, row in df.iterrows():
        entry = row.to_dict()
        entry["dataset"] = dataset_name
        json_entries.append(json.dumps(entry))
    return json_entries

admissions_json = dataframe_to_json(admissions_df, "Admissions Dataset")
medication_json = dataframe_to_json(medication_df, "Medication Dataset")
results_json = dataframe_to_json(results_df, "Results Dataset")
process_items_json = dataframe_to_json(process_items_df, "Process Items Dataset")
procedure_order_items_json = dataframe_to_json(procedure_order_items_df, "Procedure Order Items Dataset")

# Load the sentence transformer model to create embeddings
model = SentenceTransformer('all-MiniLM-L6-v2')


pc = Pinecone(api_key=os.getenv("PINECONE_API_KEY"))


if 'icu-dataset' not in pc.list_indexes().names():
    pc.create_index(
        name='icu-dataset',
        dimension=384,
        metric='cosine',
        spec=ServerlessSpec(
            cloud='aws',
            region='us-east-1'
        )
    )

index = pc.Index('icu-dataset')

def upsert_to_pinecone(json_entries, dataset_name):
    embeddings = model.encode(json_entries)
    for i, (embedding, json_entry) in enumerate(zip(embeddings, json_entries)):
        index.upsert([(f"{dataset_name.lower().replace(' ', '_')}_entry_{i}", embedding, {"data": json_entry})])

# upsert_to_pinecone(admissions_json, "Admissions Dataset")
# upsert_to_pinecone(medication_json, "Medication Dataset")
# upsert_to_pinecone(results_json, "Results Dataset")
# upsert_to_pinecone(process_items_json, "Process Items Dataset")
# upsert_to_pinecone(procedure_order_items_json, "Procedure Order Items Dataset")
#
# print("Data ingestion to Pinecone completed successfully.")
def query_pinecone(query_text, top_k=5):
    # Generate embedding for the query
    query_embedding = model.encode(query_text).tolist()

    # Query Pinecone for similar entries
    query_response = index.query(queries=[query_embedding], top_k=top_k, include_values=False, include_metadata=True)

    # Extract and print results
    for match in query_response['matches']:
        print(f"Score: {match['score']}")
        print(f"Data: {json.loads(match['metadata']['data'])}\n")


# Example usage of querying Pinecone
query_text = "How many admissions were urgent?"
query_pinecone(query_text)
