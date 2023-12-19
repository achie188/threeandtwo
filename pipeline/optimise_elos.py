import json
import itertools
from datetime import datetime, timedelta, timezone
import os
import sys
import numpy as np
import warnings
import pandas as pd

warnings.filterwarnings("ignore", category=DeprecationWarning)
location = os.getcwd()

sys.path.append('/Users/achie188/Library/CloudStorage/GitHub/Personal/threeandtwo')
file_path= location + r'/data/mlb.csv'

from outputs.to_gsheets import send_to_gsheet
from pipeline.elos import get_elos



#Optimisation Controls
steps = 10
range_around_best = steps * 3
reset = 'Yes'


params_path = location + r'/inputs/best_parameters.json'
if os.path.exists(params_path) and os.path.getsize(params_path) > 0:
    with open(params_path, 'r') as file:
        best_parameters = json.load(file)
else:
    best_parameters = {}


df = pd.read_csv(file_path)


two_years_ago = datetime.now() - timedelta(days=365 * 2)

# Initialize with the loaded best parameters
best_accuracy = {}
best_k_factor = {}
best_home_ad = {}


df = df.drop_duplicates(subset=['dateEvent', 'strHomeTeam', 'strAwayTeam'])

best_accuracy = best_parameters.get('accuracy', 0)
best_k_factor = best_parameters.get('k_factor', 24)
best_home_ad = best_parameters.get('home_ad', 50)

initial_k_factor, initial_home_ad = best_k_factor, best_home_ad

# Create a range of values around the initial best values
home_ad_range = np.arange(np.clip(initial_home_ad - range_around_best, 5, None), np.clip(initial_home_ad + range_around_best, 5, None), steps)
k_factor_range = [15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25]
home_ad_range = [30, 40, 50, 60, 70, 80, 90, 100]

best_accuracy = 0 if reset == "Yes" else best_accuracy

num_iterations = len(list(itertools.product(k_factor_range, home_ad_range)))
x = 1


for k_factor, home_ad in itertools.product(k_factor_range, home_ad_range):
    optimisation_params = [home_ad, k_factor]
    current_elo_ranks, current_elo_matches = get_elos(df, optimisation_params, optimise='Yes')
    
    current_elo_matches['date_help'] = pd.to_datetime(current_elo_matches['date'])
    current_elo_matches = current_elo_matches.sort_values(by='date_help')
    recent_matches = current_elo_matches[current_elo_matches['date_help'] > two_years_ago]

    count_true = (recent_matches['correct_WL'] == True).sum()
    count_false = (recent_matches['correct_WL'] == False).sum()

    wl_accuracy = count_true / (count_true + count_false)

    print(f"({x}/{num_iterations}) % Accuracy: {wl_accuracy * 100:.2f}%, K Factor: {k_factor}, Home Advantage: {home_ad}")

    # Update best values if the current combination has higher accuracy
    if wl_accuracy > best_accuracy:
        best_accuracy, best_accuracy = wl_accuracy, wl_accuracy
        best_k_factor, best_home_ad = k_factor, home_ad
    
    x += 1

print(f"Accuracy: {best_accuracy * 100:.2f}% - Best values: K Factor: {best_k_factor}, Home Advantage: {best_home_ad}, ")


# Save the best parameters and accuracies to a JSON file
best_parameters = {
    'accuracy': best_accuracy,
    'k_factor': best_k_factor,
    'home_ad': best_home_ad
}

params_path = location + r'/inputs/best_parameters.json'
with open(params_path, 'w') as file:
    json.dump(best_parameters, file)

best_parameters_df = pd.DataFrame.from_dict(best_parameters, orient='index')
best_parameters_df['country'] = best_parameters_df.index

# send_to_gsheet(best_parameters_df, "Football_control", "Optimal_parameters")