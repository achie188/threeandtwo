import pandas as pd


def make_features(df):

    #Rest Days
    df['date'] = pd.to_datetime(df['date'])

    combined_matches = pd.concat([df[['match_num', 'date', 'team1']].rename(columns={'team1': 'team'}),
                                df[['match_num', 'date', 'team2']].rename(columns={'team2': 'team'})])

    combined_matches.sort_values(by='date', inplace=True)
    combined_matches['rest_days'] = combined_matches.groupby('team')['date'].diff().dt.days

    elo_at_match = df.merge(combined_matches[['rest_days', 'team', 'date']], left_on=['team1', 'date'], right_on=['team', 'date'], how='left')
    elo_at_match = elo_at_match.rename(columns={'rest_days': 'home_rest_days'})

    elo_at_match['home_rest_days'] = elo_at_match['home_rest_days'].fillna(21).clip(upper=21)

    elo_at_match = elo_at_match.merge(combined_matches[['rest_days', 'team', 'date']], left_on=['team2', 'date'], right_on=['team', 'date'], how='left')
    elo_at_match = elo_at_match.rename(columns={'rest_days': 'away_rest_days'})

    elo_at_match['away_rest_days'] = elo_at_match['away_rest_days'].fillna(21).clip(upper=21)

    elo_at_match.drop(['team_x', 'team_y'], axis=1, inplace=True)

    elo_at_match = elo_at_match.drop_duplicates(subset=['date', 'team1', 'team2'])

    return elo_at_match
