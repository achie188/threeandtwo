import pandas as pd

def format_results(df):

    #rename columns
    df = df.rename(columns={'strEvent': 'Match'})
    df = df.rename(columns={'strHomeTeam': 'Home'})
    df = df.rename(columns={'strAwayTeam': 'Away'})
    df = df.rename(columns={'intHomeScore': 'H'})
    df = df.rename(columns={'intAwayScore': 'A'})
    df = df.rename(columns={'dateEvent': 'Date'})
    df = df.rename(columns={'strTime': 'Time'})


    #arrange by date
    df = df.sort_values(by='Date', ascending=False)

    #column order
    df = df[['Date', 'Time', 'Match', 'Home', 'H', 'A', 'Away']]

    return df

