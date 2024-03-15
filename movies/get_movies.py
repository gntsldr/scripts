from dotenv import load_dotenv
import csv
import json
import os
import requests


load_dotenv()  # Load environment variables from .env


def get_movie_list(api_key, base_url):
    headers = {'X-Api-Key': api_key}
    url = f"{base_url}/api/v3/movie"
    
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        movies = response.json()
        return movies
    except requests.exceptions.RequestException as e:
        print(f"Error: {e}")
        return None


def save_movies_to_file(movies, filename='movie_list.json'):
    with open(filename, 'w') as file:
        json.dump(movies, file, indent=4)
    print(f"{len(movies)} movies list exported to {filename}")


def parse_and_write_to_csv(movies, filename='movie_list.csv'):
    with open(filename, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['title', 'year', 'tmdbid', 'imdbid'])  # write header
        sorted_movies = sorted(movies, key=lambda x: x['title'])  # sort the movies by title
        for movie in sorted_movies:
            writer.writerow([movie['title'], movie['year'], movie['tmdbId']])
    print(f"{len(movies)} movies list exported to {filename}")


def main():
    api_key = os.getenv('RADARR_API_KEY')  # Replace with your Radarr API key
    base_url = "https://radarr.batmaninc.duckdns.org"  # Replace with your Radarr base URL
    
    movies = get_movie_list(api_key, base_url)
    if movies:
        save_movies_to_file(movies)
        #parse_and_write_to_csv(movies)


if __name__ == "__main__":
    main()
