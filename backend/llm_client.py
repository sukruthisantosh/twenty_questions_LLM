"""LLM client wrapper for the candidate API."""
import os
import time
import requests
from dotenv import load_dotenv

load_dotenv()

BASE_URL = "https://candidate-llm.extraction.artificialos.com/v1/responses"
CANDIDATE_API_KEY = os.getenv("CANDIDATE_API_KEY")
MAX_RETRIES = 3
RETRY_DELAY = 1


class LLMError(Exception):
    """Custom exception for LLM API errors."""
    pass


def call_llm(messages, model="gpt-5-mini-2025-08-07", max_retries=MAX_RETRIES):
    """Call the LLM API with retry logic."""
    if not CANDIDATE_API_KEY:
        raise LLMError("CANDIDATE_API_KEY not found in environment variables")
    
    last_error = None
    
    for attempt in range(max_retries):
        try:
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
            
            if response.status_code == 200:
                result = response.json()
                
                if result.get('output') and len(result['output']) > 1:
                    text_content = result['output'][1]['content'][0]['text']
                    return text_content.strip()
                
                raise LLMError("Invalid API response format")
            
            elif response.status_code == 429:
                wait_time = RETRY_DELAY * (2 ** attempt)
                if attempt < max_retries - 1:
                    time.sleep(wait_time)
                    continue
                raise LLMError(f"Rate limited. Status: {response.status_code}")
            
            else:
                response.raise_for_status()
        
        except requests.exceptions.Timeout:
            last_error = "Request timed out"
            if attempt < max_retries - 1:
                time.sleep(RETRY_DELAY * (attempt + 1))
                continue
        
        except requests.exceptions.RequestException as e:
            last_error = str(e)
            if attempt < max_retries - 1:
                time.sleep(RETRY_DELAY * (attempt + 1))
                continue
        
        except Exception as e:
            raise LLMError(f"Unexpected error: {e}")
    
    raise LLMError(f"API call failed after {max_retries} attempts: {last_error}")


if __name__ == "__main__":
    test_messages = [
        {"role": "user", "content": "Tell me about strawberries."}
    ]
    
    result = call_llm(test_messages)
    print(result)

