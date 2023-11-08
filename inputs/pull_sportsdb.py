
import pandas as pd
import requests
import os

location = os.getcwd()

# Replace 'YOUR_API_KEY' with your actual API key
api_key = '3'


def get_baseball_results():
    # Assuming the API endpoint and parameters for the 2023-2024 MLB season
    url = f'https://www.thesportsdb.com/api/v1/json/3/eventsseason.php?id=4424&s=2023'

    # Making the GET request to fetch data
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        
        # Assuming 'events' contains the list of events/games
        if 'events' in data:
            # Convert the JSON data to a Pandas DataFrame
            df = pd.DataFrame(data['events'])
            
            # To save the DataFrame to a CSV file
            file_path = location + r'/outputs/mlb_2023_2024.csv'
            df.to_csv(file_path, index=False)
            
        else:
            print("No 'events' data found in the response.")
    else:
        print("Failed to fetch data from the API.")

    return df