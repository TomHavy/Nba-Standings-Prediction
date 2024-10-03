
import pickle
import random

import pandas as pd
import numpy as np

from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import(
    classification_report, 
    accuracy_score,
)
from sklearn.model_selection import (
    GridSearchCV, 
    StratifiedKFold
)

def preprocessing(
        data,
        conference,
    ):
    data = data.drop(['team_full_name', 'winner', 'not_top_players', 'total_salary'], axis=1)

    data = data.query(f'`conference` == "{conference}"')

    data = data.drop(['conference'], axis=1)

    return data

def train(
        data,
        conference,
        id,
    ):
    # data = data.query('Season >= 2010')
    data = pd.get_dummies(data, columns=['team'], drop_first=False)
    data['ranking'] = data['ranking'].astype(int)
    data = data.query('Season != 2025')

    # print(data.tail(3))

    X = data.drop(['ranking'], axis=1)  
    y = data['ranking']

    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)
    
    X_train, X_test, y_train, y_test = train_test_split(X_scaled, y, train_size=0.75, test_size=0.25, random_state=38)
    print(f"Training shape: {X_train.shape()}")
    
    param_grid = {
    'max_depth': [80, 100, 110,150,200],
    'min_samples_leaf': [3, 4, 5, 8],
    'min_samples_split': [6, 8, 10, 12],
    'n_estimators': [100, 200, 300, 500, 1000, 1200]
    }

    cv = StratifiedKFold(n_splits=3) 

    grid_search = GridSearchCV(
        RandomForestClassifier(), 
        param_grid=param_grid,
        cv=cv, 
        n_jobs=-1, 
        verbose=1,
    ) 

    grid_search.fit(X_train, y_train) 
    print(grid_search.best_estimator_) 
    print(grid_search.best_params_) 

    with open(f"models/{id}_{conference}_grid_search_rf_class.pkl", "wb") as file:
        pickle.dump(grid_search, file)

    y_pred = grid_search.predict(X_test)

    # Evaluate the model
    print(f"[{conference}] Model evaluation")
    print(classification_report(y_test, y_pred))
    accuracy = accuracy_score(y_test, y_pred)
    print(f'Accuracy: {accuracy}')
    print(f"Model saved as 'models/{id}_{conference}_grid_search_rf_class.pkl'\n")

def pred(
        model,
        data,
        conf,
    ):
    data = data.drop(['team_full_name', 'winner','not_top_players', 'total_salary'], axis=1)

    new_season_data = pd.get_dummies(data, columns=['team'], drop_first=False)

    new_season_data = new_season_data.query(f'Season == 2025 & conference == "{conf}"')
    new_season_data.drop(['conference'], axis=1, inplace=True)

    # print(new_season_data.head(3))

    new_season_teams = data.query('Season == 2025')['team']

    new_season_data.drop(['ranking'], axis=1, inplace=True)

    # print(new_season_data.head(3))
    # print(new_season_data.info())

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

def main():
    
    id = random.randint(1000, 9999)
    data = pd.read_csv('data/2007_2025_avg_odds_salary_players_champ_rk_po.csv', index_col=0)

    for conf in ['WEST','EAST']:    
        # processed_data = preprocessing(data,conf)
        # train(
        #     processed_data,
        #     conf,
        #     id,
        # )

        with open(f"models/7818_{conf}_grid_search_rf_class.pkl", "rb") as file:
            model = pickle.load(file)

            pred_df = pred(
                model, 
                data,
                conf,
            )
            print(pred_df)
            
if __name__ == "__main__":
    main()