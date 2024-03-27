"""
This module contains functions for fetching TV show data from the Sonarr API
and saving it to a JSON file.
"""

import csv
import json
import os

import requests
from dotenv import load_dotenv


load_dotenv()  # Load environment variables from .env


def get_show_list(api_key: str, base_url: str) -> list[dict]:
    """
    Get the list of TV shows from the Sonarr API.

    Args:
        api_key (str): The Sonarr API key.
        base_url (str): The base URL of the Sonarr API.

    Returns:
        list: A list of TV shows.
    """
    headers = {"X-Api-Key": api_key}
    url = f"{base_url}/api/v3/series"

    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        shows: list[dict] = response.json()
        return shows
    except requests.exceptions.RequestException as e:
        print(f"Error: {e}")
        return []


def save_shows_to_file(shows: list[dict], filename: str = "show_list.json"):
    """
    Save the list of TV shows to a JSON file.

    Args:
        shows (list): The list of TV shows to save.
        filename (str, optional): The name of the output file.
        Defaults to "show_list.json".
    """
    with open(filename, "w", encoding="utf-8") as file:
        json.dump(shows, file, indent=4)
    print(f"{len(shows)} shows exported to {filename}")


def write_shows_to_csv(shows: list[dict], filename: str = "show_list.csv"):
    """
    Parse the TV show list and write it to a CSV file.

    Args:
        shows (list): The list of TV shows to parse and write.
        filename (str, optional): The name of the output CSV file.
        Defaults to "show_list.csv".
    """
    with open(filename, "w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(["Title", "Year", "TVDB ID"])
        sorted_shows = sorted(shows, key=lambda x: x["title"])
        for show in sorted_shows:
            writer.writerow([show["title"], show["year"], show["tvdbId"]])
    print(f"{len(shows)} shows exported to {filename}")


def main():
    """
    Main function to fetch TV show list, save to JSON, and parse to CSV.
    """
    api_key = os.getenv("SONARR_API_KEY")  # Environment variable
    base_url = os.getenv("SONARR_BASE_URL")  # Environment variable
    if api_key and base_url:
        shows: list[dict] = get_show_list(api_key, base_url)
        if shows:
            save_shows_to_file(shows)
            write_shows_to_csv(shows)
        else:
            print("No TV shows found")
    else:
        print("API key or base URL not found")


if __name__ == "__main__":
    main()
