"""Script to test object selection by calling the LLM directly."""
import sys
import os
import json
import time
from datetime import datetime

# Add project root to path
project_root = os.path.dirname(__file__)
sys.path.insert(0, project_root)

from backend.llm_client import call_llm
from backend.prompts import get_set_object_prompt

def get_chosen_object():
    """Get the object chosen by LLM Player 1 by calling LLM directly."""
    try:
        prompt = get_set_object_prompt()
        messages = [{"role": "user", "content": prompt}]
        result = call_llm(messages)
        if result:
            return result.strip()
        return None
    except Exception as e:
        print(f"Error: {e}")
        return None

def main():
    """Run the test multiple times and store results."""
    num_tests = 20
    results = []
    
    print(f"Testing object selection {num_tests} times...")
    
    for i in range(num_tests):
        print(f"Test {i+1}/{num_tests}...", end=" ", flush=True)
        obj = get_chosen_object()
        if obj:
            results.append({
                "test_number": i + 1,
                "object": obj,
                "timestamp": datetime.now().isoformat()
            })
            print(f"✓ {obj}")
        else:
            print("✗ Failed")
        time.sleep(1)  # Small delay between requests
    
    
    # Print summary
    print(f"\n{'='*50}")
    print(f"Results saved to {output_file}")
    print(f"Total successful: {len(results)}/{num_tests}")
    
    # Count object frequencies
    object_counts = {}
    for result in results:
        obj = result["object"].lower().strip()
        object_counts[obj] = object_counts.get(obj, 0) + 1
    
    print(f"\nObject frequency:")
    for obj, count in sorted(object_counts.items(), key=lambda x: x[1], reverse=True):
        print(f"  {obj}: {count}")

if __name__ == "__main__":
    main()
