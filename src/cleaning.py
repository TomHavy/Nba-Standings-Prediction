import pandas as pd

from utils import *
from bs4 import BeautifulSoup

def clean_roster(
        roster,
        team,
        team_names,
    ):

    roster['ht'] = roster['Ht'].apply(height_to_inches)
    
    roster['birth_year'] = pd.to_datetime(roster['Birth Date']).dt.year

    roster['age'] = roster['Season']- roster['birth_year'] -1

    roster['exp'] = roster['Exp'].replace('R', 0)

    roster['exp'] = roster['exp'].round().astype(int)

    roster['team'] = team

    roster['team_full_name'] = roster['team'].map(team_names)
    
    roster.drop(columns=['College','No.','Player','Pos','Birth Date','Birth','birth_year'], inplace=True)

    return roster

def clean_salaries(salaries):
    
    salaries = salaries.head(25).copy()

    salaries.rename(columns={"Unnamed: 1":"player_name"}, inplace=True)
    
    salaries.loc[:, 'Salary'] = salaries['Salary'].fillna(0)

    salaries.loc[:, 'Salary'] = salaries['Salary'].replace({r'\$': '', ',': ''}, regex=True).astype(int)

    salaries = salaries.sort_values(by='Salary', ascending=False)

    salaries = salaries.drop(columns=['Rk'])

    return salaries

def clean_champions(df):

    nba_champions = df[[('Unnamed: 0_level_0', 'Year'), ('Finals', 'Champion')]]
    nba_champions.columns = ['Year', 'Champion']

    nba_champions = nba_champions[nba_champions.Year.notna()]

    nba_champions.Year = nba_champions.Year.astype(int)

    return nba_champions

def clean_ranking(df):
    df = df.sort_values(by='W/L%', ascending=False)
    
    df.rename(columns={df.columns[0]: 'team_full_name'}, inplace=True)

    df = df[~df['team_full_name'].str.contains('Division|Conference', na=False)]

    df[df.columns[0]] = df[df.columns[0]].replace({r'\*': ''}, regex=True)
    
    df = df.reset_index(drop=True)

    df['ranking'] = df.index + 1

    df['ranking'] = df['ranking'].astype(int)

    df = df[['Season',df.columns[0], 'conference','ranking']]
    return df
