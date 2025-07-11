from guidebook import api_requestor
import json
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# get api key from environment variable (.env)
API_KEY = os.getenv('GUIDEBOOK_API_KEY')

# Use https://github.com/Guidebook/guidebook-api-python


def filter_session_data(sessions):
    """Filter sessions to keep only the properties we need"""
    filtered_sessions = []
    
    for session in sessions:
        # Print all available properties for the first session (for debugging)
        # if len(filtered_sessions) == 0:
        #     print("Available properties in session:")
        #     for key in session.keys():
        #         print(f"  - {key}")
        #     print()
        
        # Define which properties to keep
        filtered_session = {
            'id': session.get('id'),
            'name': session.get('name'),
            'description': session.get('description_html'),
            'start_time': session.get('start_time'),
            'locations': session.get('locations'),
            'schedule_tracks': session.get('schedule_tracks'),
        }
        
        # Remove None values (optional)
        filtered_session = {k: v for k, v in filtered_session.items() if v is not None}
        
        filtered_sessions.append(filtered_session)
    
    return filtered_sessions


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

    # Filter sessions to keep only needed properties
    filtered_sessions = filter_session_data(all_sessions)
    print(f"Filtered sessions to keep only essential properties")

    # Sort sessions by start_time
    filtered_sessions.sort(key=lambda session: session.get('start_time', ''))
    print(f"Sessions sorted by start_time")

    # Save filtered sessions to a file with pretty formatting
    output_path = "../public/schedule.json"
    with open(output_path, "w") as json_file:
        json.dump({
            "total_sessions": len(filtered_sessions),
            "pages_fetched": page_count,
            "sessions": filtered_sessions
        }, json_file, indent=2)
    print(f"Filtered sessions saved to {output_path}")
    


if __name__ == "__main__":
    main()
