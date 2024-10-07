import pickle

import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd

from sklearn.inspection import permutation_importance
from sklearn.metrics import(
    classification_report, 
    accuracy_score,
)

def preprocessing(
        data,
        conference,
    ):
    data = data.drop(['team_full_name', 'winner', 'not_top_players', 'total_salary'], axis=1)

    data = data.query(f'`conference` == "{conference}"')

    data = data.drop(['conference'], axis=1)

    return data

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

def plot_team_ranking_trend(team_name, df):
    # Filter the DataFrame for the input team
    team_df = df[df['team'] == team_name]

    # Sort by season to make sure the years are in chronological order
    team_df = team_df.sort_values(by='Season')

    # Plotting
    plt.figure(figsize=(10, 6))
    plt.plot(team_df['Season'], team_df['ranking'], marker='o', linestyle='-', color='b')
    
    # Invert the Y-axis so that rank 1 is on top and rank 15 is on bottom
    plt.gca().invert_yaxis()
    
    # Add labels and title
    plt.xlabel('Season', fontsize=12)
    plt.ylabel('Ranking', fontsize=12)
    plt.title(f'Ranking Trend for {team_name}', fontsize=14)
    
    # Show plot
    plt.grid(True)
    plt.xticks(team_df['Season'], rotation=45)
    plt.show()
    
def feature_importance(model, X, y):
    # Calculate permutation importance
    perm_importance = permutation_importance(model, X, y, n_repeats=30, random_state=42)

    # Create a DataFrame for permutation importance
    perm_importance_df = pd.DataFrame({
        'Feature': X.columns,
        'Importance': perm_importance.importances_mean
    }).sort_values(by='Importance', ascending=False)

    print(perm_importance_df)   

def save_model(
        model,
        model_type,
        conference,
        id,
    ):
    with open(f"models/{model_type}/{id}_{conference}_grid_search_{model_type}_class.pkl", "wb") as file:
        pickle.dump(model, file)

def evaluate_model(
            X_test,
            y_test,
            conference,
            model_type,
            model,
            rank_map
        ):
    if model_type =='xgb':
        inverse_rank_map = {v: k for k, v in rank_map.items()}  

        y_pred = model.predict(X_test)
        y_pred = pd.Series(y_pred).replace(inverse_rank_map)

    else:
        y_pred = model.predict(X_test)

    # Evaluate the model
    print(f"[{conference}] Model evaluation")
    print(classification_report(y_test, y_pred))
    accuracy = accuracy_score(y_test, y_pred)
    print(f'Accuracy: {accuracy}')
