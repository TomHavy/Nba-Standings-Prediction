import numpy as np
import pandas as pd

def pred(
        model,
        data,
        conf,
    ):

    # data = data.query('Season >= 2013')
    data = data.drop(['team_full_name', 'winner','not_top_players', 'total_salary'], axis=1)
    data = data.query(f'conference == "{conf}"')
    data.team.value_counts()

    new_season_data = pd.get_dummies(data, columns=['team'], drop_first=False)

    new_season_data = new_season_data.query(f'Season == 2025')
    new_season_data.drop(['conference'], axis=1, inplace=True)
    new_season_data.info()

    # print(new_season_data.head(3))

    new_season_teams = data.query('Season == 2025')['team']

    new_season_data.drop(['ranking'], axis=1, inplace=True)

    # new_season_data.info()

    class_proba = model.predict_proba(new_season_data.values)

    # Calculate predicted scores as the maximum probability for each team
    predicted_scores = np.max(class_proba, axis=1)

    # Add a small noise to ensure uniqueness
    noise = np.random.uniform(0, 1e-5, size=predicted_scores.shape[0])

    new_season_data['adjusted_score'] = predicted_scores + noise
    
    new_season_data['predicted_rank'] = new_season_data['adjusted_score'].rank(method='first', ascending=False).astype(int)

    new_season_data['team'] = new_season_teams

    new_season_data = new_season_data[['team','adjusted_score','predicted_rank']].sort_values(by='predicted_rank')

    return new_season_data