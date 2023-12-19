import pandas as pd
import numpy as np
from math import sqrt


def calculate_result(row):
    if pd.isnull(row['intHomeScore']) or pd.isnull(row['intAwayScore']) or row['intHomeScore'] == 'Cancelled':
        return 99
    elif float(row['intHomeScore']) > float(row['intAwayScore']):
        return 1
    elif float(row['intHomeScore']) < float(row['intAwayScore']):
        return 0
    else:
        return 0.5
    



def calculate_elo(df, params, optimise='no'):

    initial_elo = 1200
    
    df['strResult'] = df.apply(calculate_result, axis=1)

    elo_at_match_data = []

    team_ratings = {team: initial_elo for team in pd.concat([df['strHomeTeam'], df['strAwayTeam']]).unique()}

    def expected_result(rating1, rating2):
        return 1 / (1 + 10 ** ((rating2 - rating1) / 400))

    for index, match in df.iterrows():
        team1 = match['strHomeTeam']
        team2 = match['strAwayTeam']
        result = match['strResult']
        country = match['strCountry']
        # margin = abs(match['intHomeScore'] - match['intAwayScore'])
        pre_t1_rating = team_ratings[team1]
        pre_t2_rating = team_ratings[team2]

        if optimise == 'no':
            home_ad = params.get('home_ad')
            k_factor = params.get('k_factor')
        else:
            home_ad = params[0]
            k_factor = params[1]

        
        expected_team1 = expected_result(team_ratings[team1] + home_ad, team_ratings[team2])
        expected_team2 = expected_result(team_ratings[team2], team_ratings[team1] + home_ad)

        if result < 99:
            if result == 1:
                actual_team1 = 1
                actual_team2 = 0
            else:
                actual_team1 = 0
                actual_team2 = 1

            team_ratings[team1] += k_factor * (actual_team1 - expected_team1)
            team_ratings[team2] += k_factor * (actual_team2 - expected_team2)

            if optimise == 'no':
                params['home_ad'] += k_factor * (actual_team1 - expected_team1) * 0.0075

        higher_rated_team_won = None

        if result != 99:
            higher_rated_team_won = (
                (result == 1 and expected_team1 > expected_team2) or
                (result == 0 and expected_team2 > expected_team1)
            )



        elo_at_match_data.append({
            'date': match['dateEvent'],
            'season': match['strSeason'],
            'elo_team1': pre_t1_rating,
            'team1_%': expected_team1,
            'team1': team1,
            'score_pt1': match['intHomeScore'],
            'score_pt2': match['intAwayScore'],
            'team2': team2,
            'team2_%': expected_team2,
            'elo_team2': pre_t2_rating,
            'ground': match['strVenue'],
            'league': match['strLeague'],
            'home_ad': home_ad,
            'k_factor': k_factor,
            'result': result,
            'correct_WL': higher_rated_team_won,
        })

    # Convert the final Elo ratings to a DataFrame
    elo_ranks = pd.DataFrame(list(team_ratings.items()), columns=['Team', 'Elo Rating'])
    
    # Create a DataFrame with Elo ratings at each match
    elo_at_match = pd.DataFrame(elo_at_match_data)

    return elo_ranks, elo_at_match


def get_elos(df, params, optimise='no'):

    elo_rankings_df = pd.DataFrame()
    elo_matches_df = pd.DataFrame()

    df['date'] = pd.to_datetime(df['dateEvent'])
    df = df.sort_values(by='date')

    elo_ranks, elo_at_match = calculate_elo(df, params, optimise)

    elo_ranks.sort_values(by='Elo Rating', ascending=False, inplace=True)
    elo_ranks['Rank'] = range(1, len(elo_ranks) + 1)

    elo_ranks = elo_ranks[['Rank', 'Team', 'Elo Rating']]
    
    elo_rankings_df = pd.concat([elo_rankings_df, elo_ranks], ignore_index=True)
    elo_matches_df = pd.concat([elo_matches_df, elo_at_match], ignore_index=True)
    elo_matches_df['match_num'] = elo_matches_df.index

    elo_matches_df = elo_matches_df.sort_values(by='date')

    return elo_rankings_df, elo_matches_df