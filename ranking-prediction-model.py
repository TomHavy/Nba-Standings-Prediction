# %%
# import modules
import pandas as pd
from predict_rank import *

# %%
# load the cleaned data and do more FE

data = pd.read_csv('data/2008_2025_avg_odds_salary_players_champ_rk.csv', index_col=0)
to_round_columns = ['avg_age', 'avg_exp', 'avg_weight', 'avg_height', 'median_salary']
# data[to_round_columns] = data[to_round_columns].round(0).astype(int)
data = data.query('Season > 2021')

west_data = data.query('`conference` == "WEST"')
east_data = data.query('`conference` == "EAST"')
display(data)

# %%
# predict west

west_predicted_df = predict(west_data)

display(west_predicted_df[['team', 'adjusted_score', 'final_rank']].sort_values('final_rank'))

# %%
# predict east

east_predicted_df = predict(east_data)

display(east_predicted_df[['team', 'adjusted_score', 'final_rank']].sort_values('final_rank'))

# %%
