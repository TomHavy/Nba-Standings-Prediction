import pandas as pd
from bs4 import BeautifulSoup

from cleaning import *
from utils import *
from scrap import *

def scrap(start, end):
    team_conference = get_team_conference()

    end += 1

    seasons_list = [year for year in range(start, end)]

    all_rosters = scrape_all_rosters(start,end)
    all_avg_roster = team_avg_roster(all_rosters)
    all_avg_roster.to_csv(f"data/temp/{start}_{end-1}_avg_roster.csv")

    all_preseason_odds = scrape_all_preseason_odds(start,end)[["Team","Odds"]]
    all_avg_n_odds = pd.merge(all_avg_roster, all_preseason_odds, left_on='team_full_name', right_on='Team', how='left')
    all_avg_n_odds.drop(columns='Team', inplace=True)
    all_avg_n_odds.to_csv(f"data/temp/{start}_{end-1}_avg_n_odds.csv")

    all_salaries = scrape_all_salaries(start,end)
    all_salaries.to_csv(f"data/temp/{start}_{end-1}_salaries_stats.csv")

    all_top_players = find_top_players(all_salaries)
    team_salary_stats = all_salaries.groupby(['team', 'Season']).agg(
        highest_salary=('Salary', 'max'),
        median_salary=('Salary', 'median'),
        total_salary=('Salary', 'sum'),
        
    ).reset_index()
    all_team_salary_stats = pd.merge(team_salary_stats, all_top_players, on=['team', 'Season'], how="left")
    all_avg_odds_salary_players = pd.merge(all_avg_n_odds, all_team_salary_stats,on=['team', 'Season'], how='left')

    all_team_championships = scrape_all_nba_championships(seasons_list)
    all_avg_odds_salary_players_champ = all_avg_odds_salary_players.merge(all_team_championships, on=['team', 'Season'], how='left')
    all_avg_odds_salary_players_champ.to_csv(f"data/temp/{start}_{end-1}_avg_odds_salary_players_champ.csv")

    all_ranking = all_scrape_ranking(seasons_list)
    all_avg_odds_salary_players_champ_rk = all_avg_odds_salary_players_champ.merge(all_ranking, on=['team_full_name', 'Season'], how='left')
    all_avg_odds_salary_players_champ_rk.to_csv(f"data/temp/{start}_{end-1}_avg_odds_salary_players_champ_rk.csv")

def main():

    start = 2008
    end = 2009

    scrap(start,end)

    df1 = pd.read_csv('data/2010_2025_avg_odds_salary_players_champ_rk.csv', index_col=False)
    df2 = pd.read_csv('data/temp/2008_2009_avg_odds_salary_players_champ_rk.csv',  index_col=False)

    final_df = concatenate_df(df1,df2)

    final_df.to_csv(f"data/2008_2025_avg_odds_salary_players_champ_rk.csv")

if __name__ == "__main__":
    main()