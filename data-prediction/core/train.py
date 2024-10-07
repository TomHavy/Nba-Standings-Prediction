import xgboost as xgb
import pandas as pd

from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import (
    GridSearchCV, 
    StratifiedKFold
)
from core.functions import(
    save_model,
    evaluate_model,
)

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

    X_train, X_test, y_train, y_test = train_test_split(
        X_scaled, 
        y,
        train_size=0.8, 
        test_size=0.2, 
        random_state=38,
    )

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

    save_model(
        model,
        model_type,
        conference,
        id
    )
    
    evaluate_model(
        X_test,
        y_test,
        conference,
        model_type,
        model,
        rank_map,
    )
