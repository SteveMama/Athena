import json
import os
from groq import Groq
from dotenv import load_dotenv
from pymongo import MongoClient
import re

load_dotenv()

groq_api_key = os.getenv("GROQ_API_KEY")
mongodb_uri = os.getenv("MONGODB_URI")

groq_client = Groq(api_key=groq_api_key)
mongo_client = MongoClient(mongodb_uri)
db = mongo_client.icu


def fetch_data_from_mongo(query):
    results = db.patients.find(query)
    return [result for result in results]


def get_collection_schema(collection_name, sample_size=5):
    collection = db[collection_name]
    sample_docs = collection.aggregate([{"$sample": {"size": sample_size}}])
    schema = []
    for doc in sample_docs:
        schema.append(doc)
    print(f"Sample schema for collection '{collection_name}':")
    print(json.dumps(schema, indent=4))


def answer_question(question):
    chat_completion = groq_client.chat.completions.create(
        messages=[
            {
                "role": "system",
                "content": "You are a helpful assistant. Generate a MongoDB query based on the user's question. Return the query in a JSON format that can be directly parsed."
            },
            {
                "role": "user",
                "content": f"Question: {question}"
            }
        ],
        model="llama-3.1-70b-versatile",
        temperature=0.5,
        top_p=1,
        stop=None,
        stream=False,
    )
    answer_get = chat_completion.choices[0].message.content
    print("Generated response from LLM:", answer_get)

    query_match = re.search(r'\{.*\}', answer_get, re.DOTALL)
    if not query_match:
        print("Error: The response from the LLM was not a valid JSON query.")
        return

    query_str = query_match.group()
    try:
        query = json.loads(query_str)
    except json.JSONDecodeError:
        print("Error: Failed to parse the JSON query.")
        return

    print("Generated MongoDB Query:", query)

    fetched_data = fetch_data_from_mongo(query)

    context = "\n".join([json.dumps(entry) for entry in fetched_data])

    # Use Groq to get a response from the LLM
    chat_completion = groq_client.chat.completions.create(
        messages=[
            {
                "role": "system",
                "content": "You are a helpful assistant. Use the provided context to answer questions accurately."
            },
            {
                "role": "user",
                "content": f"Here is the context: {context}\n\nQuestion: {question}"
            }
        ],
        model="llama-3.1-70b-versatile",
        temperature=0.5,
        top_p=1,
        stop=None,
        stream=False,
    )

    answer = chat_completion.choices[0].message.content
    return answer


if __name__ == "__main__":
    user_question = "which patients received Amoxicillin?"
    response = answer_question(user_question)
    if response:
        print(response)

    get_collection_schema('patients')
