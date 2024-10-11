
import random

import pandas as pd

from pathlib import Path
from core.predict import pred
from core.train import train
from core.functions import(
    preprocessing,
    save,
    evaluate,
)

def main():
    
    id = random.randint(1000, 9999)
    data = pd.read_csv('data/2007_2025_avg_odds_salary_players_champ_rk_po_avg_rk_cleaned.csv')
    model_type = 'xgb'

    base_dir = f"models/{model_type}/{id}"
    Path(base_dir).mkdir(parents=True, exist_ok=True)
    # data = data.query('Season >= 2018')

    for conf in ['WEST','EAST']:  
        model_path = f"{base_dir}/{conf}_grid_search_{model_type}_class.pkl"
  
        X_train, X_test, y_train, y_test = preprocessing(
            data,
            conf,
        )
         
        model = train(
            X_train,
            y_train,
            model_type,
        )  

        save(
            model,
            model_path,
        )
        
        evaluate(
            model,
            X_test,
            y_test,
        )
        
        pred(
            model_path, 
            data,
            conf,
        )

            
if __name__ == "__main__":
    main()