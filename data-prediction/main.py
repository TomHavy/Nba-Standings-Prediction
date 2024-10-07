
import pickle
import random

import pandas as pd

from core.functions import preprocessing
from core.predict import pred
from core.train import train

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