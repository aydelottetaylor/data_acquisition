# data_acquisition
Tools for collecting and preprocessing basketball team statistics from Sports Reference for STAT 386.

## Purpose
This repository contains scripts and resources for obtaining and preprocessing data for a STAT 386 course project. Its primary goal is to provide a structured and reproducible approach to data acquisition, ensuring that all relevant datasets are collected, cleaned, and prepared for analysis.

The repository includes a Python script that scrapes comprehensive team statistics from Sports Reference, compiling them into a standardized format for further use in statistical modeling and analysis.

## Contents
- `scraper.py`: A Python script that scrapes basketball team data from Sports Reference and saves it in a .csv.
- `requirements.txt`: A list of Python packages required to run the data acquisition scripts.
- `README.md`: This file, providing an overview of the repository and its contents.
- `data/`: A directory where the acquired data files are stored.
- `data/{date}-team_stats.csv`: A csv file containing the team stats scraped from today's date.

## Usage
To use the data acquisition scripts, follow these steps:
1. Clone the repository to your local machine.
2. Install the required Python packages using pip:
    ```
    pip install -r requirements.txt
    ```
3. Run the `scraper.py` script to acquire the data:
    ```
    python scraper.py
    ```
4. The acquired data will be saved in the `data/` directory.

## Data Included In Final CSV  
The final CSV file includes the following columns representing advanced and traditional team statistics:
- team_name
- opponent_pace
- opponent_offensive_rating
- opponent_free_throw_attempt_rate
- opponent_three_point_attempt_rate
- opponent_true_shooting_percentage
- opponent_team_rebound_percentage
- opponent_assist_percentage
- opponent_steal_percentage
- opponent_block_percentage
- opponent_effective_field_goal_percentage
- opponent_turnover_percentage
- opponent_offensive_rebound_percentage
- opponent_free_throws_per_field_goal_attempt
- pace
- offensive_rating
- free_throw_attempt_rate
- three_point_attempt_rate
- true_shooting_percentage
- team_rebound_percentage
- assist_percentage
- steal_percentage
- block_percentage
- effective_field_goal_percentage
- turnover_percentage
- offensive_rebound_percentage
- free_throws_per_field_goal_attempt
- opponent_field_goals
- opponent_field_goals_attempted
- opponent_field_goal_percentage
- opponent_three_point_field_goals
- opponent_three_point_field_goals_attempted
- opponent_three_point_percentage
- opponent_free_throws
- opponent_free_throws_attempted
- opponent_free_throw_percentage
- opponent_offensive_rebounds
- opponent_team_rebounds
- opponent_assists
- opponent_steals
- opponent_blocks
- opponent_turnovers
- opponent_personal_fouls
- games
- wins
- losses
- win_percentage
- simple_rating_system
- strength_of_schedule
- wins_conf
- losses_conf
- home_wins
- home_losses
- wins_visitor
- losses_visitor
- team_points
- opponent_points
- minutes_played
- field_goals
- field_goals_attempted
- field_goal_percentage
- three_point_field_goals
- three_point_field_goals_attempted
- three_point_percentage
- free_throws
- free_throws_attempted
- free_throw_percentage
- offensive_rebounds
- team_rebounds
- assists
- steals
- blocks
- turnovers
- personal_fouls
- conference
- points_per_game
- opponent_points_per_game
- margin_of_victory
- offensive_srs
- defensive_srs
- offensive_rating_adjusted
- defensive_rating_adjusted
- net_rating_adjusted
- date

---

## License
This project is licensed under the MIT License.

Copyright (c) 2025 Taylor Aydelotte

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the “Software”), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED “AS IS”, WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
THE SOFTWARE.
