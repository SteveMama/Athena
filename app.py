import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from groq import Groq
import os
from dotenv import load_dotenv


load_dotenv()

# Load datasets
datasets = {
    'procedures': pd.read_csv('Amsterdam_dataset/Procedure_Order_Items_Dataset.csv'),
    'medications': pd.read_csv('Amsterdam_dataset/Medication_Dataset.csv'),
    'processes': pd.read_csv('Amsterdam_dataset/Process_Items_Dataset.csv'),
    'admissions': pd.read_csv('Amsterdam_dataset/Admissions_Dataset.csv')
}

# Initialize Groq client
client = Groq(api_key=os.getenv('GROQ_API_KEY'))



def classify_query(query):
    response = client.chat.completions.create(
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user",
             "content": f"Classify the following query into one of these categories: Information Retrieval, Statistical Analysis, or Visualization without any explaination\n\nQuery: {query}"}
        ],
        model="llama3-8b-8192",
        temperature=0.5,
        max_tokens=50
    )
    return response.choices[0].message.content.strip()


def retrieve_information(query, datasets):
    response = client.chat.completions.create(
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user",
             "content": f"Convert the following natural language query to a pandas query:\n\nQuery: {query}"}
        ],
        model="llama3-8b-8192",
        temperature=0.5,
        max_tokens=200
    )
    pandas_query = response.choices[0].message.content.strip()
    result = eval(pandas_query)
    return result


def perform_statistical_analysis(query, datasets):
    response = client.chat.completions.create(
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user",
             "content": f"Generate a statistical analysis plan for the following query:\n\nQuery: {query}"}
        ],
        model="llama3-8b-8192",
        temperature=0.5,
        max_tokens=200
    )
    analysis_plan = response.choices[0].message.content.strip()
    result = eval(analysis_plan)
    return result


def create_visualization(query, datasets):
    response = client.chat.completions.create(
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user",
             "content": f"Generate a Python code snippet using matplotlib or seaborn to visualize the following query:\n\nQuery: {query}"}
        ],
        model="llama3-8b-8192",
        temperature=0.5,
        max_tokens=300
    )
    visualization_code = response.choices[0].message.content.strip()
    exec(visualization_code)
    plt.savefig('visualization.png')
    plt.close()
    return 'visualization.png'


def generate_response(query, result):
    response = client.chat.completions.create(
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user",
             "content": f"Generate a natural language response for the following query and result:\n\nQuery: {query}\n\nResult: {result}"}
        ],
        model="llama3-8b-8192",
        temperature=0.7,
        max_tokens=300
    )
    return response.choices[0].message.content.strip()


def main():
    while True:
        query = input("Enter your query (or 'quit' to exit): ")
        if query.lower() == 'quit':
            break

        query_type = classify_query(query)
        print("query_type", query_type)
        if query_type == "Information Retrieval":
            result = retrieve_information(query, datasets)
        elif query_type == "Statistical Analysis":
            result = perform_statistical_analysis(query, datasets)
        elif query_type == "Visualization":
            result = create_visualization(query, datasets)

        response = generate_response(query, result)
        print(response)

        if query_type == "Visualization":
            print(f"Visualization saved as {result}")


if __name__ == "__main__":
    main()