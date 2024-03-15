from dotenv import load_dotenv
import json
import os
import requests


load_dotenv()  # Load environment variables from .env


def get_tvshow_list(api_key, base_url):
    headers = {'X-Api-Key': api_key}
    url = f"{base_url}/api/v3/series"
    
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        tvshows = response.json()
        return tvshows
    except requests.exceptions.RequestException as e:
        print(f"Error: {e}")
        return None


def save_tvshows_to_file(tvshows, filename='tvshow_list.json'):
    with open(filename, 'w') as file:
        json.dump(tvshows, file, indent=4)
    print(f"{len(tvshows)} shows exported to {filename}")


def main():
    api_key = os.getenv('SONARR_API_KEY') # Replace with your Sonarr API key
    base_url = "https://sonarr.batmaninc.duckdns.org"  # Replace with your Sonarr base URL
    
    tvshows = get_tvshow_list(api_key, base_url)
    if tvshows:
        save_tvshows_to_file(tvshows)


if __name__ == "__main__":
    main()
