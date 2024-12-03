import json
import os
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

groq_api_key = os.getenv("GROQ_API_KEY")

client = Groq(api_key=groq_api_key)

input_directory = "output_json"
json_files = [file for file in os.listdir(input_directory) if file.endswith('.json')]

json_data = []
for json_file in json_files:
    with open(os.path.join(input_directory, json_file), 'r') as f:
        json_data.extend(json.load(f))

def answer_question(question):
    context = "\n".join([json.dumps(entry) for entry in json_data])
    #print(context)

    chat_completion = client.chat.completions.create(
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
    user_question = "Are there any patients that require urgent attention for their CT scan?"
    response = answer_question(user_question)
    print(response)
