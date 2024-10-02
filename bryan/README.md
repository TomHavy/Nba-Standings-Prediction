## Aim
We aim to train a Random Forest Regressor model that does the following:

- Input: Stats of 2 different teams from the season 1 year before
- Output: Pts diff of home minus away for this year

## Data
- Running `pull_data.ipynb` will scrape the relevant data from https://www.basketball-reference.com/ and save files inside /data/ accordingly
- Running `wrangle_data.ipynb` will create the final dataset to be trained, named `training_data.csv`
- `helper.py` assumes the `nba.sqlite` file has been downloaded from https://www.kaggle.com/datasets/wyattowalsh/basketball


## Others
Using a vnev is recommended, though not explicitly stated in this README.