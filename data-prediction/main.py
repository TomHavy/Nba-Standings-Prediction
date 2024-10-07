
import pickle
import random

import pandas as pd

from pathlib import Path
from core.predict import pred
from core.train import train
from core.functions import(
    preprocessing,
    save_model,
    evaluate_model,
)

def main():
    
    id = random.randint(1000, 9999)
    data = pd.read_csv('data/2007_2025_avg_odds_salary_players_champ_rk_po_avg_rk_cleaned.csv')
    model_type = 'rf'

    base_dir = f"models/{model_type}/{id}"
    Path(base_dir).mkdir(parents=True, exist_ok=True)
    
    for conf in ['WEST']:  
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

        save_model(
            model,
            model_path,
        )
        
        evaluate_model(
            model,
            X_test,
            y_test,
            conf,
        )
        
        with open(model_path, "rb") as file:
            model = pickle.load(file)
            pred_df = pred(
                model, 
                data,
                conf,
            )
            
            print(pred_df)
            
if __name__ == "__main__":
    main()