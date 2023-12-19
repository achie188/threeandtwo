
import pandas as pd
import requests
import os
import json

location = os.getcwd()
file_path= location + r'/data'

api_file_path = location + r'/.logins/sports_db_key.json'

with open(api_file_path, 'r') as file:
    api_key_data = json.load(file)

api_key = api_key_data.get('api_key')


def get_all_seasons(league_id):
    url = f'https://www.thesportsdb.com/api/v1/json/3/search_all_seasons.php?id={league_id}'

    try:
        response = requests.get(url)
        data = response.json()

        # Check if the request was successful
        if response.status_code == 200 and 'seasons' in data:
            # Filter out seasons before 1900
            filtered_seasons = [season for season in data['seasons'] if int(season['strSeason'][:4]) >= 1900]
            return filtered_seasons
        else:
            print(f"Error: {data.get('message', 'Unknown error')}")
            return None

    except Exception as e:
        print(f"An error occurred: {e}")
        return None
    

def get_results(league_id, season):
    url = f'https://www.thesportsdb.com/api/v1/json/{api_key}/eventsseason.php?id={league_id}&s={season}'
    try:
        response = requests.get(url)
        data = response.json()

        # Check if the request was successful
        if response.status_code == 200 and 'events' in data:
            return pd.DataFrame(data['events'])
        else:
            print(f"Error: {data.get('message', 'Unknown error')}")
            return None

    except Exception as e:
        print(f"An error occurred: {e}")
        return None
    

def get_all_results(league_id):

    all_results = []

    # Get all seasons for the specified league
    seasons = get_all_seasons(league_id)

    if seasons:
        # Iterate through each season and fetch results
        for season_info in seasons:
            season = season_info['strSeason']
            results_df = get_results(league_id, season)

            # Check if the returned dataframe is empty
            if results_df is None or results_df.empty:
                break

            # Append the current season's results to the list
            all_results.append(results_df)

        # Concatenate all DataFrames in the list
        if all_results:
            all_results_df = pd.concat(all_results, ignore_index=True)

            unique_values = all_results_df['strLeague'].unique()
            print(unique_values)

            # Save to CSV using the league name
            csv_filename = f'mlb.csv'
            csv_filepath = os.path.join(file_path, csv_filename)
            all_results_df.to_csv(csv_filepath, index=False)
            print(f"Results saved for MLB")
        else:
            print(f"No results found for MLB")
    else:
        print(f"No seasons found for MLB.")

    return all_results_df


def get_CY_results():

    league_id = '4424'
    seasons = get_all_seasons(league_id)

    season = seasons[len(seasons)-1]
    season = season['strSeason']

    results_df = get_results(league_id, season)

    return results_df