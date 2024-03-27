"""
This module contains functions for fetching movie data from the Radarr API
and saving it to a JSON file.
"""

import csv
import json
import os

import requests
from dotenv import load_dotenv


load_dotenv()  # Load environment variables from .env


def get_movie_list(api_key: str, base_url: str) -> list[dict]:
    """
    Get the list of movies from the Radarr API.

    Args:
        api_key (str): The Radarr API key.
        base_url (str): The base URL of the Radarr API.

    Returns:
        list: A list of movies.
    """
    headers = {"X-Api-Key": api_key}
    url = f"{base_url}/api/v3/movie"

    try:
        response: requests.Response = requests.get(
            url, headers=headers, timeout=10
        )
        response.raise_for_status()
        movies: list[dict] = response.json()
        return movies
    except requests.exceptions.RequestException as e:
        print(f"Error: {e}")
        return []


def save_movies_to_file(movies: list[dict], filename: str = "movie_list.json"):
    """
    Save the list of movies to a JSON file.

    Args:
        movies (list): The list of movies to save.
        filename (str, optional): The name of the output JSON file.
        Defaults to "movie_list.json".
    """
    with open(filename, "w", encoding="utf-8") as file:
        json.dump(movies, file, indent=4)
    print(f"{len(movies)} movies exported to {filename}")


def write_movies_to_csv(movies: list[dict], filename: str = "movie_list.csv"):
    """
    Parse the movie list and write it to a CSV file.

    Args:
        movies (list): The list of movies to parse and write.
        filename (str, optional): The name of the output CSV file.
        Defaults to "movie_list.csv".
    """
    with open(filename, "w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(["Title", "Year", "TMDB ID"])
        sorted_movies = sorted(movies, key=lambda x: x["title"])
        for movie in sorted_movies:
            writer.writerow([movie["title"], movie["year"], movie["tmdbId"]])
    print(f"{len(movies)} movies exported to {filename}")


def main():
    """
    Main function to fetch movie list, save to JSON, and parse to CSV.
    """
    api_key = os.getenv("RADARR_API_KEY")  # Environment variable
    base_url = os.getenv("RADARR_BASE_URL")  # Environment variable
    if api_key and base_url:
        movies: list[dict] = get_movie_list(api_key, base_url)
        if movies:
            save_movies_to_file(movies)
            write_movies_to_csv(movies)
        else:
            print("No movies found")
    else:
        print("API key or base URL not found")


if __name__ == "__main__":
    main()
