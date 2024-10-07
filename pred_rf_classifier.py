
import pickle
import random

import pandas as pd
import numpy as np
import xgboost as xgb

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
        model_type='rf',
    ):
    data = data.query('Season >= 2019')
    data.team.value_counts()

    data = pd.get_dummies(data, columns=['team'], drop_first=False)
    data = data.query('Season != 2025')
    data['ranking'] = data['ranking'].astype(int)


    # print(data.tail(3))
    # print(data.info())
    print(data.Season.unique())
    X = data.drop(['ranking'], axis=1)  
    y = data['ranking']

    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)

    if model_type == 'xgb':
        rank_map = {i: i-1 for i in range(1, 16)}
        y = y.replace(rank_map)

    X_train, X_test, y_train, y_test = train_test_split(X_scaled, y, train_size=0.8, test_size=0.2, random_state=38)
    # print(f"Training shape: {X_train.shape}")
    # print(f"Testing shape: {X_test.shape}")
    # print("Training label distribution:\n", pd.Series(y_train).value_counts())
    # print("Test label distribution:\n", pd.Series(y_test).value_counts())

    rf_param_grid = {
    'max_depth': [80, 100, 110,150,200,300],
    'min_samples_leaf': [3, 4, 5, 8],
    'min_samples_split': [6, 8, 10, 12],
    'n_estimators': [200, 500, 1000, 1200,1500]
    }

    xgb_param_grid = {
        'max_depth': [3, 4, 5, 6],
        'learning_rate': [0.01, 0.1, 0.2],
        'n_estimators': [100, 200, 300, 500],
        'colsample_bytree': [0.6, 0.8, 1.0],
    }

    # cv = StratifiedKFold(n_splits=2) 

    # RandomForestClassifier good params
    # model = RandomForestClassifier(max_depth=80, min_samples_leaf=3, min_samples_split=6, n_estimators=300)

    # model = GridSearchCV(
    #     RandomForestClassifier(),
    #     param_grid=rf_param_grid,
    #     cv=2,
    #     n_jobs=-1,
    #     verbose=2,
    # )
    if model_type == 'rf':
            # RandomForestClassifier
            model = GridSearchCV(
                RandomForestClassifier(),
                param_grid=rf_param_grid,
                # cv=cv,
                n_jobs=-1,
                verbose=1,
            )
    elif model_type == 'xgb':
        model = GridSearchCV(
            xgb.XGBClassifier(),
            param_grid=xgb_param_grid,
            # cv=cv,
            n_jobs=-1,
            verbose=1,
        )
    else:
        raise ValueError("Invalid model_type! Use 'rf' for RandomForest or 'xgb' for XGBoost.")

    model.fit(X_train, y_train) 
    print(model.best_estimator_) 
    print(model.best_params_) 

    with open(f"models/{model_type}/{id}_{conference}_grid_search_{model_type}_class.pkl", "wb") as file:
        pickle.dump(model, file)

    if model_type =='xgb':
        inverse_rank_map = {v: k for k, v in rank_map.items()}  

        y_pred = model.predict(X_test)
        y_pred = pd.Series(y_pred).replace(inverse_rank_map)

    else:
        y_pred = model.predict(X_test)

    # Evaluate the model
    print(f"[{conference}] Model evaluation")
    print(classification_report(y_test, y_pred))
    accuracy = accuracy_score(y_test, y_pred)
    print(f'Accuracy: {accuracy}')
    print(f"Model saved as 'models/{model_type}/{id}_{conference}_grid_search_rf_class.pkl'\n")

def pred(
        model,
        data,
        conf,
    ):
    data = data.query('Season >= 2019')
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

def main():
    
    id = random.randint(1000, 9999)
    data = pd.read_csv('data/2007_2025_avg_odds_salary_players_champ_rk_po.csv', index_col=0)
    model_type = 'rf'

    for conf in ['WEST','EAST']:    
        processed_data = preprocessing(data,conf)
        train(
            processed_data,
            conf,
            id,
            model_type,
        )

        with open(f"models/{model_type}/{id}_{conf}_grid_search_{model_type}_class.pkl", "rb") as file:
            model = pickle.load(file)
            # print(model.best_estimator_)
            pred_df = pred(
                model, 
                data,
                conf,
            )
            print(pred_df)
            
if __name__ == "__main__":
    main()