import time
import io
import requests
import pandas as pd

from bs4 import BeautifulSoup
from selenium import webdriver
from utils import (
    get_team_conference,
    get_team_names,
    get_nb_po,
    team_avg_roster,
    find_top_players,
)
from cleaning import (
    clean_roster,
    clean_salaries,
    clean_champions,
    clean_ranking,
    clean_po,
)

def scrape_roster(season):
    # https://www.basketball-reference.com/teams/DAL/2025.html

    all_data = pd.DataFrame()
    team_names = get_team_names(season)

    for team in team_names:

        url = f"https://www.basketball-reference.com/teams/{team}/{season}.html"

        response = requests.get(url)
        # print(url)

        if response.status_code == 200:
            soup = BeautifulSoup(response.content, 'html.parser')
            table = soup.find('table', {'id': 'roster'})

            if table:
                df = pd.read_html(io.StringIO(str(table)))[0]

                df['Season'] = season
                
                df = clean_roster(df,team,team_names)

                all_data = pd.concat([all_data, df], ignore_index=True)

            else:
                print(f"No table found for {season}")

        else:
            print(f"Failed to retrieve data for {season} and team {team} : {response}")

        time.sleep(4)

    return all_data

def scrape_preseason_odds(season):
    # https://www.basketball-reference.com/leagues/NBA_2025_preseason_odds.html

    all_data = pd.DataFrame()

    url = f"https://www.basketball-reference.com/leagues/NBA_{season}_preseason_odds.html"

    response = requests.get(url)

    # print(url)

    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')
        table = soup.find('table', {'id': 'NBA_preseason_odds'})

        if table:
            df = pd.read_html(io.StringIO(str(table)))[0]

            all_data = pd.concat([all_data, df], ignore_index=True)

        else:
        
            print(f"No table found for {season}")

    else:
        print(f"Failed to retrieve data for {season} : {response}")

    return all_data

def scrape_salaries(
        season,
        driver,
    ):
    # https://www.basketball-reference.com/teams/CHO/2025.html

    all_data = pd.DataFrame()
    team_names = get_team_names(season)
    
    for team in team_names:

        url = f"https://www.basketball-reference.com/teams/{team}/{season}.html"

        driver.get(url)

        time.sleep(5)

        soup = BeautifulSoup(driver.page_source, 'html.parser')

        div = soup.find('div', {'id': 'div_salaries2'})
        
        if div:
            table = div.find('table', {'id': 'salaries2'})
            if table:
                df = pd.read_html(io.StringIO(str(table)))[0]
                df['Season'] = season
                df['team']= team
                df = clean_salaries(df)
                all_data = pd.concat([all_data, df], ignore_index=True)
            else:
                print(f"No table found inside the div for {team} in {season}")
        else:
            print(f"No div with id 'div_salaries2' found for {team} in {season}")
            
    return all_data

def scrape_champions():
    # https://www.basketball-reference.com/playoffs/

    df = pd.DataFrame()

    url = f"https://www.basketball-reference.com/playoffs/"

    response = requests.get(url)

    # print(url)

    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')
        table = soup.find('table', {'id': 'champions_index'})

        if table:
            df = pd.read_html(io.StringIO(str(table)))[0]
            df = clean_champions(df)
        else:
        
            print(f"No table found ")

    else:
        print(f"Failed to retrieve data: {response}")

    return df

def scrape_nb_championships(season):
    # Count number of championships for a given team and season

    team_names = get_team_names(season)
    
    nba_champions = scrape_champions()

    rev_team_names = {v: k for k, v in team_names.items()}

    nba_champions['team'] = nba_champions['Champion'].map(rev_team_names)
    
    team_championships = []
    
    for team in team_names:
        nb_total = len(nba_champions[
            (nba_champions['team'] == team) & 
            (nba_champions['Year'] <= season)
            ]
        )
        
        nb_interval = len(nba_champions[
            (nba_champions['team'] == team) & 
            (nba_champions['Year'] <= season) & 
            (nba_champions['Year'] > season-4)
            ]
        )
        
        team_championships.append({
            'team': team,
            'Season': season,
            'nb_championships': nb_total,
            'nb_champ_past_4y': nb_interval,
            'winner': len(nba_champions[
                (nba_champions['team'] == team) & 
                (nba_champions['Year'] == season)
                ]
            ),

        })
    
    df = pd.DataFrame(team_championships)
    
    return df

def scrape_ranking(season):
    # https://www.basketball-reference.com/leagues/NBA_2024_standings.html

    all_data = pd.DataFrame()

    url = f"https://www.basketball-reference.com/leagues/NBA_{season}_standings.html"

    response = requests.get(url)

    # print(url)

    for conf in ['W','E']:
        if response.status_code == 200:
            soup = BeautifulSoup(response.content, 'html.parser')
            table = soup.find('table', {'id': f"confs_standings_{conf}"})

            if table:
                df = pd.read_html(io.StringIO(str(table)))[0]
                
                df['Season'] = season
                if conf == 'W':
                    df["conference"] = "WEST" 
                else:
                    df['conference'] = "EAST"
                    
                df = clean_ranking(df)

                all_data = pd.concat([all_data, df], ignore_index=True)

            else:
                # print(f"No table found for {season}. Looking in Division Standings...")

                soup = BeautifulSoup(response.content, 'html.parser')
                table = soup.find('table', {'id': f"divs_standings_{conf}"})

                if table:
                    df = pd.read_html(io.StringIO(str(table)))[0]
                    
                    df['Season'] = season
                    if conf == 'W':
                        df["conference"] = "WEST" 
                    else:
                        df['conference'] = "EAST"
                    
                    df = clean_ranking(df)

                    all_data = pd.concat([all_data, df], ignore_index=True)
                else:
                    print(f"No table found for {season} in Division Standings.")

        else:
            print(f"Failed to retrieve data for {season} : {response}")

    return all_data

def scrape_all_rosters(
        start,
        end,
    ):
    all_rosters = pd.DataFrame()

    for season in range(start, end):  
        print(f"Scraping roster data for the {season-1}-{season} season...")

        roster = scrape_roster(season)

        if roster is not None:
            all_rosters = pd.concat([all_rosters, roster], ignore_index=True)
            
    return all_rosters

def scrape_all_preseason_odds(
        start,
        end,
    ):
    all_preseason_odds = pd.DataFrame()

    for season in range(start, end):  
        print(f"Scraping preseason odds data for the {season-1}-{season} season...")

        preseason_odds = scrape_preseason_odds(season)

        if preseason_odds is not None:
            all_preseason_odds = pd.concat([all_preseason_odds, preseason_odds], ignore_index=True)

    return all_preseason_odds

def scrape_all_salaries(
        start,
        end,
    ):

    all_salaries = pd.DataFrame()

    driver = webdriver.Chrome() 

    for season in range(start, end):  
        print(f"Scraping salary data for the {season-1}-{season} season...")

        salaries = scrape_salaries(
            season,
            driver,
        )

        if salaries is not None:
            all_salaries = pd.concat([all_salaries, salaries], ignore_index=True)

    driver.quit()
    
    return all_salaries

def scrape_all_nba_championships(seasons_list):
    
    all_team_championships = pd.DataFrame()

    for season in seasons_list:
        print(f"Scraping championship data for the {season-1}-{season} season...")

        team_names = get_team_names(season)

        team_championships = scrape_nb_championships(season)
        
        all_team_championships = pd.concat([all_team_championships, team_championships], ignore_index=True)

    return all_team_championships

def scrape_all_scrape_ranking(seasons_list):
    
    all_ranking = pd.DataFrame()

    for season in seasons_list:
        print(f"Scraping ranking data for the {season-1}-{season} season...")

        ranking = scrape_ranking(season)
        all_ranking = pd.concat([all_ranking, ranking], ignore_index=True)

    return all_ranking

def scrape_po():
    # https://www.basketball-reference.com/teams/BOS/

    team_names = get_team_names(2000)

    all_data = pd.DataFrame()
    print('Scraping Playoffs apperences data for every team...')
    
    for team in team_names:
        if team == 'BRK':
            team = 'NJN'
        elif team == 'CHO':
            team = 'CHA'
        elif team == 'NOP' or team == 'NOK':
            team = 'NOH'
        elif team == 'SEA':
            team = 'OKC'

        url = f"https://www.basketball-reference.com/teams/{team}"

        response = requests.get(url)

        # print(response)
        # print(url)

        if response.status_code == 200:
            soup = BeautifulSoup(response.content, 'html.parser')
            table = soup.find('table', {'id': team})

            if table:
                df = pd.read_html(io.StringIO(str(table)))[0]
                
                df = clean_po(df)

                all_data = pd.concat([all_data, df], ignore_index=True)

            else:
                print(f"No table found for {team}")

        else:
            print(f"Failed to retrieve data for {team} ")

        time.sleep(4)

    return all_data

def scrap_all(start, end):
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