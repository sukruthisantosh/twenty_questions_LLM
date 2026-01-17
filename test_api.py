"""
Simple API test script to verify the candidate LLM API connection.
"""
import os
import requests
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Get API key from environment variable
CANDIDATE_API_KEY = os.getenv("CANDIDATE_API_KEY")

BASE_URL = "https://candidate-llm.extraction.artificialos.com/v1/responses"
response = requests.post(
    BASE_URL,
    headers={
        "Content-Type": "application/json",
        "x-api-key": CANDIDATE_API_KEY
    },
    json={
        "model": "gpt-5-mini-2025-08-07",
        "input": [
            {
                "role": "user",
                "content": "How many times does the letter r appear in the word strawberry?"
            }
        ]
    }
)

print(response.json())

