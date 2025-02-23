import os
import requests

def generate_llama_response(data):
    API_URL = "https://api.llama.ai/chat"
    API_KEY = os.getenv("LLAMA_API_KEY")

    prompt = f"Analyze the stock market trends and sentiment scores for the given dataset: {data.to_json()}"

    headers = {"Authorization": f"Bearer {API_KEY}", "Content-Type": "application/json"}
    response = requests.post(API_URL, json={"prompt": prompt}, headers=headers)

    if response.status_code == 200:
        return response.json()["response"]
    else:
        return "LLaMA API call failed."

def get_stored_insights():
    try:
        with open("insights.txt", "r") as file:
            return file.read()
    except FileNotFoundError:
        return "No insights available."
