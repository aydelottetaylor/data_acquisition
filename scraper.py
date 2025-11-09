import pandas as pd
import requests
from bs4 import BeautifulSoup
from functools import reduce
from datetime import date
from pathlib import Path
from io import StringIO

BASE_DIR = Path(__file__).resolve().parent
today = date.today()

# Year that the urls depend on to pull from this specific season
# This season is 2025-26 so from Nov-Dec we need to add 1 to the year
YEAR = today.year + 1 if today.month >= 11 else today.year

# Generate output file path
output_dir = BASE_DIR / f"data/{today}-team_stats.csv"

# Generate urls to scrape
ratings_url = f'https://www.sports-reference.com/cbb/seasons/men/{YEAR}-ratings.html'
basic_stats_url = f'https://www.sports-reference.com/cbb/seasons/men/{YEAR}-school-stats.html'
basic_opponent_stats_url = f'https://www.sports-reference.com/cbb/seasons/men/{YEAR}-opponent-stats.html'
advanced_stats_url = f'https://www.sports-reference.com/cbb/seasons/men/{YEAR}-advanced-school-stats.html'
advanced_opponent_stats_url = f'https://www.sports-reference.com/cbb/seasons/men/{YEAR}-advanced-opponent-stats.html'


try:
    print(f"Scraping data for the {YEAR-1}-{YEAR} season . . . ")
    print("--------------------------------")

    # Requests for pages to scrape
    ratings_response = requests.get(ratings_url)
    basic_stats_response = requests.get(basic_stats_url)
    basic_opponent_stats_response = requests.get(basic_opponent_stats_url)
    advanced_stats_response = requests.get(advanced_stats_url)
    advanced_opponent_stats_response = requests.get(advanced_opponent_stats_url)
    
    # Soup for each page
    ratings_soup = BeautifulSoup(ratings_response.text, 'html.parser')
    basic_stats_soup = BeautifulSoup(basic_stats_response.text, 'html.parser')
    basic_opponent_stats_soup = BeautifulSoup(basic_opponent_stats_response.text, 'html.parser')
    advanced_stats_soup = BeautifulSoup(advanced_stats_response.text, 'html.parser')
    advanced_opponent_stats_soup = BeautifulSoup(advanced_opponent_stats_response.text, 'html.parser')

    # Get specific tables for each
    ratings_table = ratings_soup.find('table', {'id': 'ratings'})
    basic_stats_table = basic_stats_soup.find('table', {'id': 'basic_school_stats'})
    basic_opponent_stats_table = basic_opponent_stats_soup.find('table', {'id': 'basic_opp_stats'})
    advanced_stats_table = advanced_stats_soup.find('table', {'id': 'adv_school_stats'})
    advanced_opponent_stats_table = advanced_opponent_stats_soup.find('table', {'id': 'adv_opp_stats'})
    
    #### RATINGS ###
    ratings_df = pd.read_html(StringIO(str(ratings_table)))[0]
    ratings_df = ratings_df.dropna(how='all')
    ratings_df.columns = [col[1] for col in ratings_df.columns]
    ratings_df = ratings_df.loc[:, ~ratings_df.columns.str.contains('^Unnamed')]
    ratings_df = ratings_df[['School', 'Conf', 'Pts', 'Opp', 'MOV', 'OSRS', 'DSRS', 'ORtg', 'DRtg', 'NRtg']] # 'AP Rank',
    ratings_df = ratings_df.rename(columns={
        'School': 'team_name',
        'Conf': 'conference',
        'AP Rank': 'ap_rank',
        'Pts': 'points_per_game',
        'Opp': 'opponent_points_per_game',
        'MOV': 'margin_of_victory',
        'OSRS': 'offensive_srs',
        'DSRS': 'defensive_srs',
        'ORtg': 'offensive_rating_adjusted',
        'DRtg': 'defensive_rating_adjusted',
        'NRtg': 'net_rating_adjusted'
    })
    ratings_df = ratings_df[ratings_df['team_name'] != 'School']
    ratings_df['team_name'] = ratings_df['team_name'].astype(str).str.strip()
    ratings_df['team_name'] = ratings_df['team_name'].replace(
        {'': pd.NA, 'nan': pd.NA, 'NaN': pd.NA}
    )
    ratings_df = ratings_df[ratings_df['team_name'].notna()]

    # Reindex so iloc[20] is the 21st *valid* row
    ratings_df = ratings_df.reset_index(drop=True)


    ### BASIC TEAM STATS ###
    basic_stats_df = pd.read_html(StringIO(str(basic_stats_table)))[0]
    basic_stats_df = basic_stats_df.dropna(how='all')

    def abbr(col):
        # If columns are MultiIndex tuples like ('Overall','W'), transform selectively
        if not isinstance(col, tuple) or len(col) != 2:
            return col
        grp, val = col

        if grp == 'Overall' and val in {'W', 'L'}:
            return (grp, 'O. W' if val == 'W' else 'O. L')
        if grp == 'Conf.' and val in {'W', 'L'}:
            return (grp, 'C. W' if val == 'W' else 'C. L')
        if grp == 'Home' and val in {'W', 'L'}:
            return (grp, 'H. W' if val == 'W' else 'H. L')
        if grp == 'Away' and val in {'W', 'L'}:
            return (grp, 'A. W' if val == 'W' else 'A. L')  # note: 'Away', not 'Home'

        return col
    basic_stats_df.columns = basic_stats_df.columns.map(abbr)
    basic_stats_df.columns = [col[1] for col in basic_stats_df.columns]
    basic_stats_df = basic_stats_df.loc[:, ~basic_stats_df.columns.str.contains('^Unnamed')]
    basic_stats_df = basic_stats_df.drop('Rk', axis=1)

    basic_stats_df = basic_stats_df.rename(columns={
        'School': 'team_name',
        'G': 'games',
        'O. W': 'wins',
        'O. L': 'losses',
        'W-L%': 'win_percentage',
        'SRS': 'simple_rating_system',
        'SOS': 'strength_of_schedule',
        'C. W': 'wins_conf',
        'C. L': 'losses_conf',
        'H. W': 'home_wins',
        'H. L': 'home_losses',
        'A. W': 'wins_visitor',
        'A. L': 'losses_visitor',
        'Tm.': 'team_points',
        'Opp.': 'opponent_points',
        'MP': 'minutes_played',
        'FG': 'field_goals',
        'FGA': 'field_goals_attempted',
        'FG%': 'field_goal_percentage',
        '3P': 'three_point_field_goals',
        '3PA': 'three_point_field_goals_attempted',
        '3P%': 'three_point_percentage',
        'FT': 'free_throws',
        'FTA': 'free_throws_attempted',
        'FT%': 'free_throw_percentage',
        'ORB': 'offensive_rebounds',
        'TRB': 'team_rebounds',
        'AST': 'assists',
        'STL': 'steals',
        'BLK': 'blocks',
        'TOV': 'turnovers',
        'PF': 'personal_fouls'
    })
    basic_stats_df = basic_stats_df[basic_stats_df['team_name'] != 'School']
    basic_stats_df['team_name'] = basic_stats_df['team_name'].astype(str).str.strip()
    basic_stats_df['team_name'] = basic_stats_df['team_name'].replace(
        {'': pd.NA, 'nan': pd.NA, 'NaN': pd.NA}
    )
    basic_stats_df = basic_stats_df[basic_stats_df['team_name'].notna()]

    # Reindex so iloc[20] is the 21st *valid* row
    basic_stats_df = basic_stats_df.reset_index(drop=True)


    ### BASIC OPPONENT STATS ###
    opponent_basic_stats_df = pd.read_html(StringIO(str(basic_opponent_stats_table)))[0]
    opponent_basic_sttas_df = opponent_basic_stats_df.dropna(how='all')
    opponent_basic_stats_df.columns = [col[1] for col in opponent_basic_stats_df.columns]
    opponent_basic_stats_df = opponent_basic_stats_df.loc[:, ~opponent_basic_stats_df.columns.str.contains('^Unnamed')]
    opponent_basic_stats_df = opponent_basic_stats_df[['School', 'FG', 'FGA', 'FG%', '3P', '3PA', '3P%', 'FT', 'FTA', 'FT%', 'ORB', 'TRB',
                                                    'AST', 'STL', 'BLK', 'TOV', 'PF']]
    opponent_basic_stats_df = opponent_basic_stats_df.rename(columns={
        'School': 'team_name',
        'FG': 'opponent_field_goals',
        'FGA': 'opponent_field_goals_attempted',
        'FG%': 'opponent_field_goal_percentage',
        '3P': 'opponent_three_point_field_goals',
        '3PA': 'opponent_three_point_field_goals_attempted',
        '3P%': 'opponent_three_point_percentage',
        'FT': 'opponent_free_throws',
        'FTA': 'opponent_free_throws_attempted',
        'FT%': 'opponent_free_throw_percentage',
        'ORB': 'opponent_offensive_rebounds',
        'TRB': 'opponent_team_rebounds',
        'AST': 'opponent_assists',
        'STL': 'opponent_steals',
        'BLK': 'opponent_blocks',
        'TOV': 'opponent_turnovers',
        'PF': 'opponent_personal_fouls'
    })
    opponent_basic_stats_df = opponent_basic_stats_df[opponent_basic_stats_df['team_name'] != 'School']
    opponent_basic_stats_df['team_name'] = opponent_basic_stats_df['team_name'].astype(str).str.strip()
    opponent_basic_stats_df['team_name'] = opponent_basic_stats_df['team_name'].replace(
        {'': pd.NA, 'nan': pd.NA, 'NaN': pd.NA}
    )
    opponent_basic_stats_df = opponent_basic_stats_df[opponent_basic_stats_df['team_name'].notna()]

    # Reindex so iloc[20] is the 21st *valid* row
    opponent_basic_stats_df = opponent_basic_stats_df.reset_index(drop=True)


    ### ADVANCED STATS ###
    advanced_stats_df = pd.read_html(StringIO(str(advanced_stats_table)))[0]
    advanced_stats_df = advanced_stats_df.dropna(how='all')
    advanced_stats_df.columns = [col[1] for col in advanced_stats_df.columns]
    advanced_stats_df = advanced_stats_df.loc[:, ~advanced_stats_df.columns.str.contains('^Unnamed')]
    advanced_stats_df = advanced_stats_df[['School', 'Pace', 'ORtg', 'FTr', '3PAr', 'TS%', 'TRB%', 'AST%', 'STL%', 'BLK%', 'eFG%', 'TOV%',
                                        'ORB%', 'FT/FGA']]
    advanced_stats_df = advanced_stats_df.rename(columns={
        'School': 'team_name',
        'Pace': 'pace',
        'ORtg': 'offensive_rating',
        'FTr': 'free_throw_attempt_rate',
        '3PAr': 'three_point_attempt_rate',
        'TS%': 'true_shooting_percentage',
        'TRB%': 'team_rebound_percentage',
        'AST%': 'assist_percentage',
        'STL%': 'steal_percentage',
        'BLK%': 'block_percentage',
        'eFG%': 'effective_field_goal_percentage',
        'TOV%': 'turnover_percentage',
        'ORB%': 'offensive_rebound_percentage',
        'FT/FGA': 'free_throws_per_field_goal_attempt'
    })
    advanced_stats_df = advanced_stats_df[advanced_stats_df['team_name'] != 'School']
    advanced_stats_df['team_name'] = advanced_stats_df['team_name'].astype(str).str.strip()
    advanced_stats_df['team_name'] = advanced_stats_df['team_name'].replace(
        {'': pd.NA, 'nan': pd.NA, 'NaN': pd.NA}
    )
    advanced_stats_df = advanced_stats_df[advanced_stats_df['team_name'].notna()]

    # Reindex so iloc[20] is the 21st *valid* row
    advanced_stats_df = advanced_stats_df.reset_index(drop=True)


    ### OPPONENT ADVANCED STATS ###
    opponent_advanced_stats_df = pd.read_html(StringIO(str(advanced_opponent_stats_table)))[0]
    opponent_advanced_stats_df = opponent_advanced_stats_df.dropna(how='all')
    opponent_advanced_stats_df.columns = [col[1] for col in opponent_advanced_stats_df.columns]
    opponent_advanced_stats_df = opponent_advanced_stats_df.loc[:, ~opponent_advanced_stats_df.columns.str.contains('^Unnamed')]
    opponent_advanced_stats_df = opponent_advanced_stats_df[['School', 'Pace', 'ORtg', 'FTr', '3PAr', 'TS%', 'TRB%', 'AST%', 'STL%', 'BLK%', 'eFG%', 'TOV%',
                                        'ORB%', 'FT/FGA']]
    opponent_advanced_stats_df = opponent_advanced_stats_df.rename(columns={
        'School': 'team_name',
        'Pace': 'opponent_pace',
        'ORtg': 'opponent_offensive_rating',
        'FTr': 'opponent_free_throw_attempt_rate',
        '3PAr': 'opponent_three_point_attempt_rate',
        'TS%': 'opponent_true_shooting_percentage',
        'TRB%': 'opponent_team_rebound_percentage',
        'AST%': 'opponent_assist_percentage',
        'STL%': 'opponent_steal_percentage',
        'BLK%': 'opponent_block_percentage',
        'eFG%': 'opponent_effective_field_goal_percentage',
        'TOV%': 'opponent_turnover_percentage',
        'ORB%': 'opponent_offensive_rebound_percentage',
        'FT/FGA': 'opponent_free_throws_per_field_goal_attempt'
    })
    opponent_advanced_stats_df = opponent_advanced_stats_df[opponent_advanced_stats_df['team_name'] != 'School']
    opponent_advanced_stats_df['team_name'] = opponent_advanced_stats_df['team_name'].astype(str).str.strip()
    opponent_advanced_stats_df['team_name'] = opponent_advanced_stats_df['team_name'].replace(
        {'': pd.NA, 'nan': pd.NA, 'NaN': pd.NA}
    )
    opponent_advanced_stats_df = opponent_advanced_stats_df[opponent_advanced_stats_df['team_name'].notna()]

    # Reindex so iloc[20] is the 21st *valid* row
    opponent_advanced_stats_df = opponent_advanced_stats_df.reset_index(drop=True)

    print("Shape Of Each DF By Page")
    print(" -> Opponent advanced stats df:", opponent_advanced_stats_df.shape)
    print(" -> Advanced stats df:", advanced_stats_df.shape)
    print(" -> Opponent basic stats df:", opponent_basic_stats_df.shape)
    print(" -> Basic stats df:", basic_stats_df.shape)
    print(" -> Ratings df:", ratings_df.shape)
    print("--------------------------------")
    
    # Merge all dataframes together
    dfs = [opponent_advanced_stats_df, advanced_stats_df, opponent_basic_stats_df, basic_stats_df, ratings_df]
    all_stats = reduce(lambda left, right: pd.merge(left, right, on="team_name", how="outer"), dfs)
    df = all_stats.copy()    
    
    # Build a canonical team key that strips "NCAA"
    df['team_base'] = (
        df['team_name']
        .astype(str)
        .str.replace(r'\bNCAA\b', '', regex=True)
        .str.strip()
    )

    # Mark which rows had "NCAA" so we can prefer non-NCAA rows
    df['has_ncaa'] = df['team_name'].str.contains(r'\bNCAA\b', case=False, na=False)

    # Sort so non-NCAA rows come first within each team
    df = df.sort_values(['team_base', 'has_ncaa'])  # False (no NCAA) comes before True

    # For each team, coalesce columns by taking the first non-null (now prefers non-NCAA)
    def first_non_null(s: pd.Series):
        # return the first non-null value in order
        idx = s.first_valid_index()
        return s.loc[idx] if idx is not None else pd.NA
    
    agg = {
        col: first_non_null
        for col in df.columns
        if col not in ['team_name', 'team_base', 'has_ncaa']
    }

    collapsed = (
        df.groupby('team_base', as_index=False)
        .agg(agg)
        .rename(columns={'team_base': 'team_name'})
        .reset_index(drop=True)
    )

    all_stats = collapsed
    
    # Add date column
    all_stats['date'] = today

    # Check the final dataframe shape
    print(f"New shape after merging all DFs, should match (365, 84) : {all_stats.shape}")
    print("--------------------------------")

    # Save data to CSV for later
    all_stats.to_csv(output_dir, index=False)
    print(f"CSV containing data saved to: {output_dir}")
    print("--------------------------------")
    
    print("Finished successfully!")

except Exception as e:
    print(f'An exception occurred: {e}')
