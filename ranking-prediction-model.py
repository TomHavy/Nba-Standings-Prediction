# %%
# import modules
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import mean_squared_error

# %%
# load the cleaned data and do more FE

data = pd.read_csv('2023_2025_avg_odds_salary_players')

# Convert categorical variables to numeric if necessary (e.g., one-hot encoding)
data = pd.get_dummies(data, columns=['team'], drop_first=True)

# Create features and target variable
features = data.drop(['Rank'], axis=1)  # assuming 'Rank' is your target variable
target = data['Rank']

# Normalize the features
scaler = StandardScaler()
scaled_features = scaler.fit_transform(features)

# %%
# training the model
X_train, X_test, y_train, y_test = train_test_split(scaled_features, target, test_size=0.2, random_state=42)

model = RandomForestRegressor(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

y_pred = model.predict(X_test)

mse = mean_squared_error(y_test, y_pred)
print(f'Mean Squared Error: {mse}')

# %%
# predict for the upcoming season
upcoming_season_data = pd.read_csv('upcoming_nba_team_stats.csv')

# Preprocess the upcoming season data
upcoming_season_data.fillna(method='ffill', inplace=True)
upcoming_season_data = pd.get_dummies(upcoming_season_data, columns=['Team'], drop_first=True)
scaled_upcoming_data = scaler.transform(upcoming_season_data)

upcoming_season_data['Predicted Score'] = model.predict(scaled_upcoming_data)

# %%
# Ensure Unique Ranks
# Adding a small noise to ensure uniqueness
noise = np.random.uniform(0, 1e-6, size=upcoming_season_data.shape[0])
upcoming_season_data['Adjusted Score'] = upcoming_season_data['Predicted Score'] + noise

# Rank based on the adjusted scores
upcoming_season_data['Exclusive Rank'] = upcoming_season_data['Adjusted Score'].rank(method='first', ascending=False).astype(int)

print(upcoming_season_data[['Team', 'Predicted Score', 'Exclusive Rank']])
