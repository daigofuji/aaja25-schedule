from guidebook import api_requestor
import json
import os
from dotenv import load_dotenv
from datetime import datetime, timezone, timedelta

# Load environment variables from .env file
load_dotenv()

# get api key from environment variable (.env)
API_KEY = os.getenv('GUIDEBOOK_API_KEY')

# Use https://github.com/Guidebook/guidebook-api-python

def filter_session_data(sessions):
    """Filter sessions to keep only the properties we need"""
    filtered_sessions = []
    
    def parse_day_and_time(start_time_str):
        """Parse start_time to extract day and formatted time"""
        if not start_time_str:
            return "Unknown", "Unknown"
        
        try:
            # Parse the ISO datetime string as UTC
            dt = datetime.fromisoformat(start_time_str.replace('Z', '+00:00'))
            # Convert to PDT (UTC-7)
            pdt = timezone(timedelta(hours=-7))
            dt_pdt = dt.astimezone(pdt)

            date_to_day = {
                "2025-07-30": "Wed 7/30",
                "2025-07-31": "Thur 7/31", 
                "2025-08-01": "Fri 8/1",
                "2025-08-02": "Sat 8/2"
            }
            
            date_str = dt_pdt.strftime("%Y-%m-%d")
            day = date_to_day.get(date_str, f"Day {date_str}")
            
            # Format time as "11 AM PDT" style
            hour = dt_pdt.hour
            minute = dt_pdt.minute
            
            if hour == 0:
                time_str = f"12:{minute:02d} AM PDT"
            elif hour < 12:
                time_str = f"{hour}:{minute:02d} AM PDT" if minute > 0 else f"{hour} AM PDT"
            elif hour == 12:
                time_str = f"12:{minute:02d} PM PDT" if minute > 0 else "12 PM PDT"
            else:
                time_str = f"{hour-12}:{minute:02d} PM PDT" if minute > 0 else f"{hour-12} PM PDT"

            return day, time_str
            
        except Exception as e:
            print(f"Error parsing time {start_time_str}: {e}")
            return "Unknown", "Unknown"

    # get location name from location id
    location_map = {
        5055999: "REDWOOD",
        5056000: "WILLOW",
        5056001: "GRAND BALLROOM",
        5056002: "ASPEN",
        5056003: "METROPOLITAN B",
        5056005: "CEDAR",
        5056006: "METROPOLITAN A"
    }
    def get_location_name(location_id):
        """Get location name from location ID"""
        return location_map.get(location_id, "Other")
    
    def get_location_names(location_ids):
        """Get location names from a list of location IDs"""
        if not location_ids:
            return []
        if isinstance(location_ids, list):
            return [get_location_name(location_ids[0])]
        else:
            return [get_location_name(location_ids)]

    for session in sessions:
        # Parse day and time from start_time
        day, time = parse_day_and_time(session.get('start_time'))
        
        # Get location names from location IDs
        location_names = get_location_names(session.get('locations'))
        
        # Define which properties to keep
        filtered_session = {
            'id': session.get('id'),
            'name': session.get('name'),
            'description': session.get('description_html'),
            'start_time': session.get('start_time'),
            'day': day,
            'time': time,
            'locations': location_names,
            'tracks': session.get('schedule_tracks'),
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

    # save csv in ../public/schedule.csv
    csv_output_path = "../public/schedule.csv"
    with open(csv_output_path, "w") as csv_file:
        csv_file.write("id,name,day,time,locations,schedule_tracks\n")
        for session in filtered_sessions:
            # Convert locations and tracks to strings before joining
            locations_str = '|'.join(session.get('locations', []))
            tracks_str = '|'.join(str(track) for track in session.get('tracks', []))

            csv_file.write(f"{session.get('id')},\"{session.get('name')}\","
                           f"{session.get('day')},{session.get('time')},"
                           f"{locations_str},{tracks_str}\n")
    print(f"Filtered sessions saved to {csv_output_path}")

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
