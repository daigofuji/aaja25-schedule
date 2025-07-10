from guidebook import api_requestor
import json
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# get api key from environment variable (.env)
API_KEY = os.getenv('GUIDEBOOK_API_KEY')

# Use https://github.com/Guidebook/guidebook-api-python


def main():
    # Check if API key is set
    if not API_KEY:
        print("Error: GUIDEBOOK_API_KEY environment variable is not set")
        print("Please set it by running: export GUIDEBOOK_API_KEY='your_api_key_here'")
        return
    
    print(f"Using API key: {API_KEY[:10]}..." if len(API_KEY) > 10 else API_KEY)
    
    api_client = api_requestor.APIRequestor(API_KEY)

    base_url = 'https://builder.guidebook.com/open-api/v1.1/sessions/?guide=215066'
    
    all_sessions = []
    current_url = base_url
    page_count = 0
    
    while current_url:
        page_count += 1
        print(f"Fetching page {page_count}...")
        
        response = api_client.request('get', current_url)
        print(f"Page {page_count} response keys:", list(response.keys()) if isinstance(response, dict) else "Not a dict")
        
        # Extract sessions from this page
        if isinstance(response, dict) and 'results' in response:
            sessions = response.get('results', [])
            all_sessions.extend(sessions)
            print(f"Found {len(sessions)} sessions on page {page_count}")
            
            # Check for next page
            current_url = response.get('next')
            if current_url:
                print(f"Next page URL: {current_url}")
            else:
                print("No more pages")
        else:
            print("Unexpected response format")
            break
    
    print(f"\nTotal sessions collected: {len(all_sessions)} across {page_count} pages")

    # Save all sessions to a file with pretty formatting
    with open("schedule.json", "w") as json_file:
        json.dump({
            "total_sessions": len(all_sessions),
            "pages_fetched": page_count,
            "sessions": all_sessions
        }, json_file, indent=2)
    print("All sessions saved to schedule.json")
    


if __name__ == "__main__":
    main()
