"""LLM client wrapper for the candidate API."""
import os
import requests
from dotenv import load_dotenv

load_dotenv()

BASE_URL = "https://candidate-llm.extraction.artificialos.com/v1/responses"
CANDIDATE_API_KEY = os.getenv("CANDIDATE_API_KEY")


def call_llm(messages, model="gpt-5-mini-2025-08-07"):
    """Call the LLM API and return the text response."""
    response = requests.post(
        BASE_URL,
        headers={
            "Content-Type": "application/json",
            "x-api-key": CANDIDATE_API_KEY
        },
        json={
            "model": model,
            "input": messages
        },
        timeout=30
    )
    
    response.raise_for_status()
    result = response.json()
    
    if result.get('output') and len(result['output']) > 1:
        text_content = result['output'][1]['content'][0]['text']
        return text_content.strip()
    
    return ""


if __name__ == "__main__":
    test_messages = [
        {"role": "user", "content": "Tell me about strawberries."}
    ]
    
    result = call_llm(test_messages)
    print(result)

