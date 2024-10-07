import pandas as pd

from utils import (
    get_team_conference,
    get_team_names,
    team_avg_roster,
    find_top_players,
    concatenate_save_finaldf,
    get_nb_po,
)
from scrap import (
    scrape_po,
    scrape_all_rosters,
    scrape_all_preseason_odds,
    scrape_all_salaries,
    scrape_all_nba_championships,
    scrape_all_scrape_ranking,
)

def scrap(start, end):
    team_conference = get_team_conference()

    end += 1

    seasons_list = [year for year in range(start, end)]
    all_rosters = scrape_all_rosters(start,end)
    all_avg_roster = team_avg_roster(all_rosters)
    all_avg_roster.to_csv(f"data/temp/{start}_{end-1}_avg_roster.csv")

    all_preseason_odds = scrape_all_preseason_odds(start,end)[["Team","Odds"]]
    all_avg_n_odds = pd.merge(
        all_avg_roster, 
        all_preseason_odds, 
        left_on='team_full_name', 
        right_on='Team', 
        how='left',
    )
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
    all_team_salary_stats = pd.merge(
        team_salary_stats, 
        all_top_players, 
        on=['team', 'Season'], 
        how="left",
    )
    all_avg_odds_salary_players = pd.merge(
        all_avg_n_odds, 
        all_team_salary_stats,
        on=['team', 'Season'], 
        how='left',
    )

    all_team_championships = scrape_all_nba_championships(seasons_list)
    all_avg_odds_salary_players_champ = all_avg_odds_salary_players.merge(
        all_team_championships, 
        on=['team', 'Season'], 
        how='left',
    )
    all_avg_odds_salary_players_champ.to_csv(f"data/temp/{start}_{end-1}_avg_odds_salary_players_champ.csv")

    all_ranking = scrape_all_scrape_ranking(seasons_list)
    all_avg_odds_salary_players_champ_rk = all_avg_odds_salary_players_champ.merge(
        all_ranking, 
        on=['team_full_name', 'Season'], 
        how='left',
    )

    po = scrape_po()
    po_apperences = get_nb_po(po)

    all_avg_odds_salary_players_champ_rk_po = all_avg_odds_salary_players_champ_rk.merge(
        po_apperences, 
        on=['team_full_name','Season'],
        how='left',
    )
    all_avg_odds_salary_players_champ_rk_po = all_avg_odds_salary_players_champ_rk_po.sort_values(by=['team_full_name', 'Season'], ascending=[True, False])
    all_avg_odds_salary_players_champ_rk_po['nb_po_apperence'] = all_avg_odds_salary_players_champ_rk_po['nb_po_apperence'].bfill()
    all_avg_odds_salary_players_champ_rk_po['nb_po_apperence'] = all_avg_odds_salary_players_champ_rk_po['nb_po_apperence'].astype("Int64")
    all_avg_odds_salary_players_champ_rk_po.insert(16, 'nb_po_apperence', all_avg_odds_salary_players_champ_rk_po.pop('nb_po_apperence'))

    all_avg_odds_salary_players_champ_rk_po.to_csv(f"data/temp/{start}_{end-1}_avg_odds_salary_players_champ_rk_po.csv")
    print(f'Successfully collected data from {start} to {end-1} and saved in data/temp/ ')

def main():

    start = 2006
    end = 2006

    scrap(start,end)
    
    concatenate_save_finaldf(start,end)

if __name__ == "__main__":
    main()