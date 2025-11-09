## data_acquisition
Data Acquisition Repo for STAT 386

# Purpose
This repository contains scripts and resources for obtaining and preprocessing data for a STAT 386 course project. The goal is to provide a structured approach to data acquisition, ensuring that all necessary datasets are collected and prepared for analysis.

# Contents
- `scraper.py`: A Python script that scrapes data from specified web sources and saves it in a structured format.
- `requirements.txt`: A list of Python packages required to run the data acquisition scripts.
- `README.md`: This file, providing an overview of the repository and its contents.
- `data/`: A directory where the acquired data files are stored.

# Usage
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
