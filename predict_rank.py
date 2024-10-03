import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor, RandomForestClassifier
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.inspection import permutation_importance
from sklearn.svm import SVR

def feature_importance(model, X, y):
    # Calculate permutation importance
    perm_importance = permutation_importance(model, X, y, n_repeats=30, random_state=42)

    # Create a DataFrame for permutation importance
    perm_importance_df = pd.DataFrame({
        'Feature': X.columns,
        'Importance': perm_importance.importances_mean
    }).sort_values(by='Importance', ascending=False)

    print(perm_importance_df)   
    
    
def predict(data):
    new_season_teams = data.query('Season == 2025')['team']
    data = data.drop(['team_full_name', 'winner', 'conference', 'not_top_players', 'total_salary'], axis=1)
    # Convert categorical variables to numeric if necessary (e.g., one-hot encoding)
    data = pd.get_dummies(data, columns=['team'], drop_first=False)

    training_data = data.query('Season != 2025')
    new_season_data = data.query('Season == 2025')
    
    
    # Create features and target variable
    features = training_data.drop(['ranking'], axis=1)  # assuming 'ranking' is your target variable
    target = training_data['ranking']

    # Normalize the features
    scaler = StandardScaler()
    scaled_features = scaler.fit_transform(features)
    
    X_train, X_test, y_train, y_test = train_test_split(scaled_features, target, train_size=0.9, test_size=0.1, random_state=38)

    model = RandomForestRegressor(n_estimators=50, random_state=38)
    # model = SVR(kernel='rbf')
    model.fit(X_train, y_train)
    y_pred = model.predict(X_test)
    
    # Assuming y_pred and y_test are already defined from your predictions
    mse = mean_squared_error(y_test, y_pred)
    mae = mean_absolute_error(y_test, y_pred)
    rmse = np.sqrt(mse)
    r_squared = r2_score(y_test, y_pred)
    mape = np.mean(np.abs((y_test - y_pred) / y_test)) * 100

    # Print all metrics
    print(f'Mean Absolute Error (MAE): {mae}')
    print(f'Mean Squared Error (MSE): {mse}')
    print(f'Root Mean Squared Error (RMSE): {rmse}')
    print(f'R-squared: {r_squared}')
    print(f'Mean Absolute Percentage Error (MAPE): {mape}%')
    
    # feature_importance(model, X_train, y_test)
    
    # predict for the upcoming season
    new_season_data = new_season_data.drop(['ranking'], axis=1)

    # Preprocess the upcoming season data
    # new_season_data.fillna(method='ffill', inplace=True)
    # new_season_data = pd.get_dummies(new_season_data, columns=['team', 'conference'])
    # scaled_upcoming_data = scaler.transform(new_season_data)

    new_season_data['predicted_score'] = model.predict(new_season_data.values)

    # Ensure Unique Ranks
    # Adding a small noise to ensure uniqueness
    noise = np.random.uniform(0, 1e-5, size=new_season_data.shape[0])
    new_season_data['adjusted_score'] = new_season_data['predicted_score'] + noise
    new_season_data['team'] = new_season_teams

    # Rank based on the adjusted_scores
    new_season_data['final_rank'] = new_season_data['adjusted_score'].rank(method='first', ascending=True).astype(int)

    return new_season_data
    


def show_feature_correlation(data):
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