import pickle

import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd

from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
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

    data = data.query('Season != 2025')
    data['ranking'] = data['ranking'].astype(int)

    data = pd.get_dummies(data, columns=['team'], drop_first=False)

    print(data.head())
    print(data.tail(3))
    print(data.info())
    print(data.Season.unique())

    # print(f"Training shape: {X_train.shape}")
    # print(f"Testing shape: {X_test.shape}")
    # print("Training label distribution:\n", pd.Series(y_train).value_counts())
    # print("Test label distribution:\n", pd.Series(y_test).value_counts())

    X = data.drop(['ranking'], axis=1)  
    y = data['ranking']

    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)

    X_train, X_test, y_train, y_test = train_test_split(
        X_scaled, 
        y,
        train_size=0.7, 
        test_size=0.3, 
        random_state=38,
    )

    return  X_train, X_test, y_train, y_test

def show_feature_correlation(data):
    # Compute the correlation matrix
    correlation_matrix = data.corr()

    # Set up the matplotlib figure
    plt.figure(figsize=(12, 10))

    # Create a heatmap to visualize the correlations
    sns.heatmap(
        correlation_matrix, 
        annot=True, 
        fmt='.1f', 
        cmap='coolwarm', 
        square=True, 
        cbar_kws={"shrink": .8},
    )

    # Add title and labels
    plt.title('Feature Correlation Matrix', fontsize=12)
    plt.xticks(rotation=45)
    plt.yticks(rotation=45)
    plt.tight_layout()

    # Show the plot
    plt.show()

def plot_team_ranking_trend(
        team_name, 
        df,
    ):
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
    
def feature_importance(
        model, 
        X, 
        y,
    ):
    # Calculate permutation importance
    perm_importance = permutation_importance(
        model, 
        X, 
        y, 
        n_repeats=30, 
        random_state=42,
    )

    # Create a DataFrame for permutation importance
    perm_importance_df = pd.DataFrame({
        'Feature': X.columns,
        'Importance': perm_importance.importances_mean
    }).sort_values(by='Importance', ascending=False)

    print(perm_importance_df)   

def save_model(
        model,
        model_path,
    ):
    with open(model_path, "wb") as file:
        pickle.dump(model, file)

def evaluate_model(
            model,
            X_test,
            y_test,
            conference,
        ):

        # print(model.best_estimator_) 
        # print(model.best_params_) 

        y_pred = model.predict(X_test)

        # Evaluate the model
        print(f"[{conference}] Model evaluation")
        print(classification_report(y_test, y_pred))
        accuracy = accuracy_score(y_test, y_pred)
        print(f'Accuracy: {accuracy}')
