# %%
# import modules
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import mean_absolute_error, r2_score
import seaborn as sns
import matplotlib.pyplot as plt

# %%
# load the cleaned data and do more FE

data = pd.read_csv('data/2023_2024_avg_odds_salary_players_champ_rk.csv', index_col=0)
data = data.drop(['team_full_name', 'winner'], axis=1)
teams = data['team']
display(data)

# %%
# Convert categorical variables to numeric if necessary (e.g., one-hot encoding)
data = pd.get_dummies(data, columns=['team'], drop_first=False)
# data['team'] = teams
display(data)

# %%
# feature correlation

# Compute the correlation matrix
correlation_matrix = data.corr()

# Set up the matplotlib figure
plt.figure(figsize=(12, 10))

# Create a heatmap to visualize the correlations
sns.heatmap(correlation_matrix, annot=True, fmt='.1f', cmap='coolwarm', square=True, cbar_kws={"shrink": .8})

# Add title and labels
plt.title('Feature Correlation Matrix', fontsize=12)
plt.xticks(rotation=45)
plt.yticks(rotation=45)
plt.tight_layout()

# Show the plot
plt.show()

# %%
# Create features and target variable
features = data.drop(['ranking'], axis=1)  # assuming 'ranking' is your target variable
target = data['ranking']

# Normalize the features
scaler = StandardScaler()
scaled_features = scaler.fit_transform(features)

# %%
# training the model
X_train, X_test, y_train, y_test = train_test_split(scaled_features, target, test_size=0.2, random_state=42)

model = RandomForestRegressor(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

y_pred = model.predict(X_test)

# %%
# metrics calculation 

# Assuming y_pred and y_test are already defined from your predictions
mse = mean_squared_error(y_test, y_pred)
mae = mean_absolute_error(y_test, y_pred)
rmse = np.sqrt(mse)
r_squared = r2_score(y_test, y_pred)

# Calculate MAPE
mape = np.mean(np.abs((y_test - y_pred) / y_test)) * 100

# Print all metrics
print(f'Mean Absolute Error (MAE): {mae}')
print(f'Mean Squared Error (MSE): {mse}')
print(f'Root Mean Squared Error (RMSE): {rmse}')
print(f'R-squared: {r_squared}')
print(f'Mean Absolute Percentage Error (MAPE): {mape}%')

# %%
# predict for the upcoming season
upcoming_season_data = pd.read_csv('data/2025_team_info.csv', index_col=0).reset_index
upcoming_season_data = upcoming_season_data.drop(['team_full_name'], axis=1)
upcoming_teams = upcoming_season_data['team']
display(upcoming_season_data)

# %%
# Preprocess the upcoming season data
# upcoming_season_data.fillna(method='ffill', inplace=True)
upcoming_season_data = pd.get_dummies(upcoming_season_data, columns=['team'])
scaled_upcoming_data = scaler.transform(upcoming_season_data)

upcoming_season_data['predicted_score'] = model.predict(scaled_upcoming_data)

# %%
# Ensure Unique Ranks
# Adding a small noise to ensure uniqueness
noise = np.random.uniform(0, 1e-6, size=upcoming_season_data.shape[0])
upcoming_season_data['adjusted_score'] = upcoming_season_data['predicted_score'] + noise
upcoming_season_data['team'] = upcoming_teams

# Rank based on the adjusted_scores
upcoming_season_data['final_rank'] = upcoming_season_data['adjusted_score'].rank(method='first', ascending=True).astype(int)

# %%
display(upcoming_season_data[['team', 'adjusted_score', 'final_rank']].sort_values('final_rank'))

# %%

# probability of the rank
