import xgboost as xgb

from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import (
    GridSearchCV, 
    StratifiedKFold
)

def train(
        X_train,
        y_train,
        model_type,
    ):

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

    cv = StratifiedKFold(n_splits=2) 

    # RandomForestClassifier good params
    # model = RandomForestClassifier(max_depth=80, min_samples_leaf=3, min_samples_split=6, n_estimators=300)

    if model_type == 'rf':
            # RandomForestClassifier
            model = GridSearchCV(
                RandomForestClassifier(),
                param_grid=rf_param_grid,
                cv=cv,
                n_jobs=-1,
                verbose=1,
            )
    elif model_type == 'xgb':
        model = GridSearchCV(
            xgb.XGBClassifier(),
            param_grid=xgb_param_grid,
            cv=cv,
            n_jobs=-1,
            verbose=1,
        )
    else:
        raise ValueError("Invalid model_type! Use 'rf' for RandomForest or 'xgb' for XGBoost.")

    model.fit(X_train, y_train) 
    
    return model
