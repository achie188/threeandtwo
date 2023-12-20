import pandas as pd
import sys
import os
import json

from inputs.pull_sportsdb import get_CY_results
from pipeline.format_table import format_results
from outputs.to_gsheets import send_to_gsheet, clear_gsheet
from pipeline.elos import get_elos
from pipeline.ml_model import train_prediction_model, make_predictions

location = os.getcwd()

sys.path.append('/Users/achie188/Library/CloudStorage/GitHub/Personal/threeandtwo')
file_path= location + r'/data/mlb.csv'

params_path = location + r'/inputs/best_parameters.json'
with open(params_path, 'r') as file:
    best_parameters = json.load(file)



#Get latest data
print("Getting latest results")
baseball_results = get_CY_results()


#Format the dataframe
print("Formatting")
formatted_bb = format_results(baseball_results)


#Run Elos
print("Calculating rankings")
df = pd.read_csv(file_path)
elo_ranks, elo_matches = get_elos(df, best_parameters)


#ML Model
print("Running predictions")
model = train_prediction_model(elo_matches)
preds = make_predictions(model, elo_matches)


#Send to gsheets
print("Uploading")
clear_gsheet("threeandTwo Baseball Data", "Results")
clear_gsheet("threeandTwo Baseball Data", "Rankings")
clear_gsheet("threeandTwo Baseball Data", "Rankings by Match")

send_to_gsheet(formatted_bb, "threeandTwo Baseball Data", "Results")
send_to_gsheet(elo_ranks, "threeandTwo Baseball Data", "Rankings")
send_to_gsheet(preds, "threeandTwo Baseball Data", "Rankings by Match")


print("Complete")
