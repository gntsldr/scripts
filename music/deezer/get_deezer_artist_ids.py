"""
Script to use the Deezer API to retrieve the favorite artists for a given user ID
and save the artist IDs to a CSV file.

Usage:
    python get_deezer_artist_ids.py

Output:
    config/deezer_artist_ids.csv

Author: [gntsldr](https://gitlab.com/gntsldr)
"""

from dotenv import load_dotenv
import csv
import os
import requests


load_dotenv()  # Load environment variables from .env


def get_favorite_artists(user_id):
    """
    Get favorite artists for a given user ID from the Deezer API.

    Artists are retrieved in chunks of 25 due to Deezer API limits.

    Args:
        user_id (str): The user ID for which to fetch favorite artists.

    Returns:
        list: List of favorite artist IDs.
    """
    url: str = f'https://api.deezer.com/user/{user_id}/artists'
    artists: list[int] = []
    limit: int = 25
    offset: int = 0
    while True:
        params: dict = {'index': offset, 'limit': limit}
        response: requests.Response = requests.get(url, params=params)
        if response.status_code == 200:
            data: dict = response.json()
            artists.extend([artist['id'] for artist in data['data']])
            if 'next' not in data or not data['next']:
                break
            offset += limit
        else:
            print(f"Error retrieving artists: {response.status_code}")
            break
    return artists


def output_to_csv(data: list[int], filename: str):
    """
    Write artist IDs to a CSV file.

    Args:
        data (list): List of artist IDs to be written to CSV.
        filename (str): Name of the CSV file.
    """
    with open(filename, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerows([[artist] for artist in data])


if __name__ == "__main__":
    """
    Retrieves favorite artists for a given user ID from the Deezer API
    and saves the artist IDs to a CSV file.
    """
    user_id: str = os.getenv('DEEZER_USER_ID')  # Deezer user ID
    output_file: str = 'config/deezer_artist_ids.csv'
    artists: list[int] = get_favorite_artists(user_id)
    output_to_csv(artists, output_file)
    print(f"{len(artists)} Deezer artist IDs saved to '{output_file}'")

