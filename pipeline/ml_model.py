import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score
from datetime import datetime
import numpy as np

def calculate_prediction(row):
    if pd.isnull(row['win']) or pd.isnull(row['loss']) or row['score_pt1'] == 'Cancelled':
        return 99
    elif float(row['win']) > float(row['loss']):
        return 1
    elif float(row['win']) < float(row['loss']):
        return 0
    else:
        return 0.5
    

def compare_result_and_prediction(result, prediction):
    if result.equals(99):  # Use .equals() for Series comparison
        return None
    else:
        return np.equal(result, prediction)


def train_prediction_model(df):
    df = df[df['result'] != 99]
    
    result_mapping = {1: 2, 0.5: 1, 0: 0}
    df.loc[:, 'result'] = df['result'].map(result_mapping)

    # Create a feature matrix X and target variable y
    X = df[['elo_team1', 'elo_team2']]
    y = df['result'].astype(int)

    # Split the data into training and testing sets
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # Train a logistic regression model for multiclass classification
    model = LogisticRegression(multi_class='multinomial', solver='lbfgs')
    model.fit(X_train, y_train)

    # Make predictions on the test set
    y_pred = model.predict(X_test)

    # Evaluate the model
    accuracy = accuracy_score(y_test, y_pred)
    print(f' - Model accuracy: {accuracy * 100:.1f}%')

    return model


def make_predictions(model, df):
    
    now = pd.to_datetime(datetime.now().strftime('%Y-%m-%d'))
    # upcoming_df = df[df['date'] >= now]
    upcoming_df = df.copy()

    probabilities = model.predict_proba(upcoming_df[['elo_team1', 'elo_team2']])
    
    upcoming_df = upcoming_df.copy()
    upcoming_df['win'] = probabilities[:, 2]
    upcoming_df['draw'] = probabilities[:, 1] 
    upcoming_df['loss'] = probabilities[:, 0]

    upcoming_df['pred'] = upcoming_df.apply(calculate_prediction, axis=1)

    upcoming_df['correct_prediction'] = compare_result_and_prediction(upcoming_df['result'], upcoming_df['pred'])
    
    # df = df[df['date'] < now]

    # updated_df = pd.concat([df, upcoming_df], ignore_index=True)

    return upcoming_df
