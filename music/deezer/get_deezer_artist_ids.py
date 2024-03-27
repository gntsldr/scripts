"""
Script to use the Deezer API to retrieve the favorite artists for a given user ID
and save the artist IDs to a CSV file.

Usage:
    python get_deezer_artist_ids.py

Output:
    config/deezer_artist_ids.csv

Author: [gntsldr](https://gitlab.com/gntsldr)
"""

import csv
import logging
import os

import requests
from dotenv import load_dotenv

DEFAULT_OUTPUT_FILE: str = "deezer_artist_ids.csv"


load_dotenv()  # Load environment variables from .env


def get_favorite_artists() -> list[int]:
    """
    Get favorite artists for a given user ID from the Deezer API.

    Artists are retrieved in chunks of 25 due to Deezer API limits.

    Args:
        user_id (str): The user ID for which to fetch favorite artists.

    Returns:
        list: List of favorite artist IDs.
    """
    user_id = check_deezer_user_id()
    artists_api_url: str = f"https://api.deezer.com/user/{user_id}/artists"
    artists: list[int] = []
    limit: int = 25
    offset: int = 0
    while True:
        params: dict = {"index": offset, "limit": limit}
        try:
            response: requests.Response = requests.get(
                artists_api_url, params=params, timeout=30
            )
            if not response.ok:
                logging.error("HTTP Error: %s", response.status_code)
                break
            response.raise_for_status()
            data: dict = response.json()
            artists.extend([artist["id"] for artist in data["data"]])
            if not data.get("next"):
                return artists
            offset += limit
        except requests.exceptions.RequestException as e:
            logging.error("Request Error: %s", e)
            raise
    return artists


def output_to_csv(data: list[int], filename: str = "deezer_artist_ids.csv"):
    """
    Write artist IDs to a CSV file.

    Args:
        data (list): List of artist IDs to be written to CSV.
        filename (str): Name of the CSV file.
    """
    try:
        with open(filename, "w", newline="", encoding="utf-8") as file:
            writer = csv.writer(file)
            writer.writerows([[artist] for artist in data])
    except FileNotFoundError as e:
        logging.error("File not found: %s - %s", os.path.abspath(filename), e)
        raise
    except PermissionError as e:
        logging.error(
            "Permission denied: %s - %s", os.path.abspath(filename), e
        )
        raise


def check_deezer_user_id(deezer_user_id=os.getenv("DEEZER_USER_ID")) -> str:
    """
    Check the environment variable for Deezer user ID.

    Returns:
        str: Deezer user ID.
    """
    if not deezer_user_id:
        raise ValueError("DEEZER_USER_ID in .env file is required.")
    if not deezer_user_id.isnumeric():
        raise ValueError("DEEZER_USER_ID must be numeric.")
    return deezer_user_id


def check_output_file(output_file=os.getenv("OUTPUT_FILE")) -> str:
    """
    Determine the output file from environment variable or use default.

    Returns:
        str: Output file path.
    """
    if not output_file:
        output_file = DEFAULT_OUTPUT_FILE
        logging.info(
            "OUTPUT_FILE not set. Using default '%s'",
            DEFAULT_OUTPUT_FILE,
        )
    return output_file


def main():
    """
    Retrieves favorite artists for a given user ID from the Deezer API
    and saves the artist IDs to a CSV file.
    """
    output_file: str = check_output_file()
    # if not deezer_user_id:
    #    print("Missing Deezer user ID. Exiting...")
    #    return
    try:
        artists: list[int] = get_favorite_artists()
        if not artists:
            print("No artist IDs retrieved. Exiting...")
            return
        output_to_csv(artists, output_file)
        print(f"{len(artists)} Deezer artist IDs saved to '{output_file}'")
    except requests.exceptions.RequestException as e:
        logging.error("%s: %s", e.__class__.__name__, e)
    except (FileNotFoundError, PermissionError) as e:
        logging.error("%s: %s", e.__class__.__name__, e)


if __name__ == "__main__":
    main()
