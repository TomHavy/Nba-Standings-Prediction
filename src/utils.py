import pandas as pd

from bs4 import BeautifulSoup

def get_team_conference():

    team_conferences = {
    'ATL': 'EAST',
    'BOS': 'EAST',
    'BRK': 'EAST',
    'NJN': 'EAST',
    'CHA': 'EAST',
    'CHO': 'EAST',
    'CHI': 'EAST',
    'CLE': 'EAST',
    'DAL': 'WEST',
    'DEN': 'WEST',
    'DET': 'EAST',
    'GSW': 'WEST',
    'HOU': 'WEST',
    'IND': 'EAST',
    'LAC': 'WEST',
    'LAL': 'WEST',
    'MEM': 'WEST',
    'MIA': 'EAST',
    'MIL': 'EAST',
    'MIN': 'WEST',
    'NOP': 'WEST',
    'NOH': 'WEST',
    'NYK': 'EAST',
    'OKC': 'WEST',
    'ORL': 'EAST',
    'PHI': 'EAST',
    'PHO': 'WEST',
    'POR': 'WEST',
    'SAC': 'WEST',
    'SAS': 'WEST',
    'TOR': 'EAST',
    'UTA': 'WEST',
    'WAS': 'EAST'
    }

    return team_conferences

def get_team_names(season):
    if season == 2013:
        team_names = {
        'ATL': 'Atlanta Hawks',
        'BOS': 'Boston Celtics',
        'BRK': 'Brooklyn Nets',
        'CHA': 'Charlotte Bobcats',
        'CHI': 'Chicago Bulls',
        'CLE': 'Cleveland Cavaliers',
        'DAL': 'Dallas Mavericks',
        'DEN': 'Denver Nuggets',
        'DET': 'Detroit Pistons',
        'GSW': 'Golden State Warriors',
        'HOU': 'Houston Rockets',
        'IND': 'Indiana Pacers',
        'LAC': 'Los Angeles Clippers',
        'LAL': 'Los Angeles Lakers',
        'MEM': 'Memphis Grizzlies',
        'MIA': 'Miami Heat',
        'MIL': 'Milwaukee Bucks',
        'MIN': 'Minnesota Timberwolves',
        'NOH': 'New Orleans Hornets',
        'NYK': 'New York Knicks',
        'OKC': 'Oklahoma City Thunder',
        'ORL': 'Orlando Magic',
        'PHI': 'Philadelphia 76ers',
        'PHO': 'Phoenix Suns',
        'POR': 'Portland Trail Blazers',
        'SAC': 'Sacramento Kings',
        'SAS': 'San Antonio Spurs',
        'TOR': 'Toronto Raptors',
        'UTA': 'Utah Jazz',
        'WAS': 'Washington Wizards'
    }
    elif season == 2014:
        team_names = {
            'ATL': 'Atlanta Hawks',
            'BOS': 'Boston Celtics',
            'BRK': 'Brooklyn Nets',
            'CHA': 'Charlotte Bobcats',
            'CHI': 'Chicago Bulls',
            'CLE': 'Cleveland Cavaliers',
            'DAL': 'Dallas Mavericks',
            'DEN': 'Denver Nuggets',
            'DET': 'Detroit Pistons',
            'GSW': 'Golden State Warriors',
            'HOU': 'Houston Rockets',
            'IND': 'Indiana Pacers',
            'LAC': 'Los Angeles Clippers',
            'LAL': 'Los Angeles Lakers',
            'MEM': 'Memphis Grizzlies',
            'MIA': 'Miami Heat',
            'MIL': 'Milwaukee Bucks',
            'MIN': 'Minnesota Timberwolves',
            'NOP': 'New Orleans Pelicans',
            'NYK': 'New York Knicks',
            'OKC': 'Oklahoma City Thunder',
            'ORL': 'Orlando Magic',
            'PHI': 'Philadelphia 76ers',
            'PHO': 'Phoenix Suns',
            'POR': 'Portland Trail Blazers',
            'SAC': 'Sacramento Kings',
            'SAS': 'San Antonio Spurs',
            'TOR': 'Toronto Raptors',
            'UTA': 'Utah Jazz',
            'WAS': 'Washington Wizards'
        }
    elif season>2008 & season<2013:
        team_names = {
            'ATL': 'Atlanta Hawks',
            'BOS': 'Boston Celtics',
            'NJN': 'New Jersey Nets',
            'CHA': 'Charlotte Bobcats',
            'CHI': 'Chicago Bulls',
            'CLE': 'Cleveland Cavaliers',
            'DAL': 'Dallas Mavericks',
            'DEN': 'Denver Nuggets',
            'DET': 'Detroit Pistons',
            'GSW': 'Golden State Warriors',
            'HOU': 'Houston Rockets',
            'IND': 'Indiana Pacers',
            'LAC': 'Los Angeles Clippers',
            'LAL': 'Los Angeles Lakers',
            'MEM': 'Memphis Grizzlies',
            'MIA': 'Miami Heat',
            'MIL': 'Milwaukee Bucks',
            'MIN': 'Minnesota Timberwolves',
            'NOH': 'New Orleans Hornets',
            'NYK': 'New York Knicks',
            'OKC': 'Oklahoma City Thunder',
            'ORL': 'Orlando Magic',
            'PHI': 'Philadelphia 76ers',
            'PHO': 'Phoenix Suns',
            'POR': 'Portland Trail Blazers',
            'SAC': 'Sacramento Kings',
            'SAS': 'San Antonio Spurs',
            'TOR': 'Toronto Raptors',
            'UTA': 'Utah Jazz',
            'WAS': 'Washington Wizards'
        }
    elif season==2008:
        team_names = {
            'ATL': 'Atlanta Hawks',
            'BOS': 'Boston Celtics',
            'NJN': 'New Jersey Nets',
            'CHA': 'Charlotte Bobcats',
            'CHI': 'Chicago Bulls',
            'CLE': 'Cleveland Cavaliers',
            'DAL': 'Dallas Mavericks',
            'DEN': 'Denver Nuggets',
            'DET': 'Detroit Pistons',
            'GSW': 'Golden State Warriors',
            'HOU': 'Houston Rockets',
            'IND': 'Indiana Pacers',
            'LAC': 'Los Angeles Clippers',
            'LAL': 'Los Angeles Lakers',
            'MEM': 'Memphis Grizzlies',
            'MIA': 'Miami Heat',
            'MIL': 'Milwaukee Bucks',
            'MIN': 'Minnesota Timberwolves',
            'NOH': 'New Orleans Hornets',
            'NYK': 'New York Knicks',
            'SEA': 'Seattle SuperSonics',
            'ORL': 'Orlando Magic',
            'PHI': 'Philadelphia 76ers',
            'PHO': 'Phoenix Suns',
            'POR': 'Portland Trail Blazers',
            'SAC': 'Sacramento Kings',
            'SAS': 'San Antonio Spurs',
            'TOR': 'Toronto Raptors',
            'UTA': 'Utah Jazz',
            'WAS': 'Washington Wizards'
        }
    elif season<=2007:
        team_names = {
        'ATL': 'Atlanta Hawks',
        'BOS': 'Boston Celtics',
        'BRK': 'Brooklyn Nets',
        'CHO': 'Charlotte Hornets',
        'CHI': 'Chicago Bulls',
        'CLE': 'Cleveland Cavaliers',
        'DAL': 'Dallas Mavericks',
        'DEN': 'Denver Nuggets',
        'DET': 'Detroit Pistons',
        'GSW': 'Golden State Warriors',
        'HOU': 'Houston Rockets',
        'IND': 'Indiana Pacers',
        'LAC': 'Los Angeles Clippers',
        'LAL': 'Los Angeles Lakers',
        'MEM': 'Memphis Grizzlies',
        'MIA': 'Miami Heat',
        'MIL': 'Milwaukee Bucks',
        'MIN': 'Minnesota Timberwolves',
        'NOK': 'New Orleans/Oklahoma City Hornetss',
        'NYK': 'New York Knicks',
        'SEA': 'Seattle SuperSonics',
        'ORL': 'Orlando Magic',
        'PHI': 'Philadelphia 76ers',
        'PHO': 'Phoenix Suns',
        'POR': 'Portland Trail Blazers',
        'SAC': 'Sacramento Kings',
        'SAS': 'San Antonio Spurs',
        'TOR': 'Toronto Raptors',
        'UTA': 'Utah Jazz',
        'WAS': 'Washington Wizards'
    }
    else:
        team_names = {
        'ATL': 'Atlanta Hawks',
        'BOS': 'Boston Celtics',
        'BRK': 'Brooklyn Nets',
        'CHO': 'Charlotte Hornets',
        'CHI': 'Chicago Bulls',
        'CLE': 'Cleveland Cavaliers',
        'DAL': 'Dallas Mavericks',
        'DEN': 'Denver Nuggets',
        'DET': 'Detroit Pistons',
        'GSW': 'Golden State Warriors',
        'HOU': 'Houston Rockets',
        'IND': 'Indiana Pacers',
        'LAC': 'Los Angeles Clippers',
        'LAL': 'Los Angeles Lakers',
        'MEM': 'Memphis Grizzlies',
        'MIA': 'Miami Heat',
        'MIL': 'Milwaukee Bucks',
        'MIN': 'Minnesota Timberwolves',
        'NOP': 'New Orleans Pelicans',
        'NYK': 'New York Knicks',
        'OKC': 'Oklahoma City Thunder',
        'ORL': 'Orlando Magic',
        'PHI': 'Philadelphia 76ers',
        'PHO': 'Phoenix Suns',
        'POR': 'Portland Trail Blazers',
        'SAC': 'Sacramento Kings',
        'SAS': 'San Antonio Spurs',
        'TOR': 'Toronto Raptors',
        'UTA': 'Utah Jazz',
        'WAS': 'Washington Wizards'
    }
    return team_names

def height_to_inches(height):

    if pd.isna(height):
        return None
    feet, inches = map(int, height.split('-'))
    return feet * 12 + inches

def team_avg_roster(roster):
    avg_roster = roster.groupby(['team', 'team_full_name','Season']).agg(
        avg_age=('age', 'mean'),
        avg_exp=('exp', 'mean'),
        avg_weight=('Wt', 'mean'),
        avg_height=('ht', 'mean')
    ).reset_index()

    avg_roster = avg_roster[['Season','team', 'team_full_name', 'avg_age', 'avg_exp', 'avg_weight', 'avg_height']]
    
    return avg_roster

def count_top_players(
        salaries,
        threshold=20,
    ):
    # based on the teams salaries we are trying to identify the numbers of stars/top players on the team (a good example is the Phoenix Suns in 2025)

    above = salaries[salaries['salary_percentage'] > threshold].shape[0]
    below = salaries[salaries['salary_percentage'] <= threshold].shape[0]
    
    return pd.Series({'top_players': above, 'not_top_players': below})

def find_top_players(salaries):
    total_salary = salaries.groupby(['team', 'Season'])['Salary'].sum().reset_index(name='total_salary')

    salaries = salaries.merge(total_salary, on=['team', 'Season'], how='left')

    salaries['salary_percentage'] = (salaries['Salary'] / salaries['total_salary']) * 100

    top_players = salaries.groupby(['team', 'Season']).apply(count_top_players).reset_index()
    
    return top_players

def concatenate_df(
        df1,
        df2,
    ):

    df1 = df1.iloc[:, 1:]
    df2 = df2.iloc[:, 1:]
    final_df = pd.concat([df1, df2], ignore_index=True)
    final_df['ranking'] = final_df['ranking'].astype("Int64")

    return final_df