import subprocess
import sys
import warnings
from dependencies import check_and_install_dependencies
import pandas as pd
import numpy as np
import zipfile
import requests
from io import BytesIO
from tqdm import tqdm

# Check and install the necessary dependencies for the script to run
check_and_install_dependencies()

# Configure pandas to display a larger number of columns and output width
pd.set_option('display.max_columns', 500)
pd.set_option('display.width', 1000)

# List of URLs containing ATP tennis data from 2000 to 2025
# Each link contains data for a specific year in Excel or compressed (zip) format
links = ['http://tennis-data.co.uk/2000/2000.xls', 'http://tennis-data.co.uk/2001/2001.xls', 
         'http://tennis-data.co.uk/2002/2002.xls', 'http://tennis-data.co.uk/2003/2003.xls', 
         'http://tennis-data.co.uk/2004/2004.xls', 'http://tennis-data.co.uk/2005/2005.xls', 
         'http://tennis-data.co.uk/2006/2006.xls', 'http://tennis-data.co.uk/2007/2007.xls', 
         'http://tennis-data.co.uk/2008/2008.zip', 'http://tennis-data.co.uk/2009/2009.xls', 
         'http://tennis-data.co.uk/2010/2010.xls', 'http://tennis-data.co.uk/2011/2011.xls', 
         'http://tennis-data.co.uk/2012/2012.xls', 'http://tennis-data.co.uk/2013/2013.xlsx', 
         'http://tennis-data.co.uk/2014/2014.xlsx', 'http://tennis-data.co.uk/2015/2015.xlsx', 
         'http://tennis-data.co.uk/2016/2016.xlsx', 'http://tennis-data.co.uk/2017/2017.xlsx', 
         'http://tennis-data.co.uk/2018/2018.xlsx', 'http://tennis-data.co.uk/2019/2019.xlsx', 
         'http://tennis-data.co.uk/2020/2020.xlsx', 'http://tennis-data.co.uk/2021/2021.xlsx', 
         'http://tennis-data.co.uk/2022/2022.xlsx', 'http://tennis-data.co.uk/2023/2023.xlsx',
         'http://tennis-data.co.uk/2024/2024.xlsx', 'http://tennis-data.co.uk/2025/2025.xlsx']

print("Iniciando download e processamento dos dados de tênis de 2000-2025...")
df = pd.DataFrame()
# Iterate over each link to download and process the data, with progress bar using tqdm
for i, elem in enumerate(tqdm(links, desc="Baixando e processando arquivos", unit="arquivo")):
    # Special handling for compressed files (zip)
    if elem[-4:] == '.zip':
        content = requests.get(elem)
        zf = zipfile.ZipFile(BytesIO(content.content))
        temp = pd.read_excel(zf.open(zf.namelist()[0])) 
    else:
        # Direct reading for Excel files
        temp = pd.read_excel(elem) 
    # Concatenate the current year's data with accumulated data
    df = pd.concat([df, temp], ignore_index=True)

print("Download concluído. Iniciando limpeza e processamento dos dados...")

# Fill missing values for match format (best of 3 or 5 sets)
df['Best of'] = df['Best of'].fillna(3)
# Filter only completed matches
df = df[df['Comment'] == 'Completed'].reset_index(drop=True)
# Remove matches with missing player rankings
df = df[~df['WRank'].isnull()].reset_index(drop=True)
df = df[~df['LRank'].isnull()].reset_index(drop=True)
# Remove matches with missing scores in the first two sets
df = df[~df['W1'].isnull()].reset_index(drop=True)
df = df[~df['W2'].isnull()].reset_index(drop=True)
df = df[~df['L1'].isnull()].reset_index(drop=True)
df = df[~df['L2'].isnull()].reset_index(drop=True)
# Fill missing scores in additional sets with zeros
df[['W3', 'W4', 'W5', 'L3', 'L4', 'L5']] = df[['W3', 'W4', 'W5', 'L3', 'L4', 'L5']].fillna(0)

# Convert odds columns to numeric format
for col in ['CBW', 'GBW', 'IWW', 'SBW', 'B&WW', 'EXW', 'PSW', 'UBW', 'LBW', 'SJW', 'AvgW',
            'CBL', 'GBL', 'IWL', 'SBL', 'B&WL', 'EXL', 'PSL', 'UBL', 'LBL', 'SJL', 'AvgL']:
    df[col] = pd.to_numeric(df[col], errors='coerce')

# Fill missing odds using the average from other bookmakers
df['B365W'] = df['B365W'].fillna(df[['CBW', 'GBW', 'IWW', 'SBW', 'B&WW', 'EXW', 'PSW', 'UBW', 'LBW', 'SJW']].mean(axis=1)).fillna(df['AvgW'])
df['B365L'] = df['B365L'].fillna(df[['CBL', 'GBL', 'IWL', 'SBL', 'B&WL', 'EXL', 'PSL', 'UBL', 'LBL', 'SJL']].mean(axis=1)).fillna(df['AvgL'])

# Create an index column to alternate between winner and loser
df['ind'] = [(lambda x: x % 2)(x) for x in range(len(df))]

# Function to convert empty strings to zeros
def checkempty(str):
    """
    Converts empty strings to zero
    Args:
        str: Value to be checked
    Returns:
        0 if the value is a blank space, otherwise returns the original value
    """
    if str == ' ':
        return 0
    return str

# Apply the check function and convert score columns to integers
df['W3'] = df['W3'].apply(checkempty)
df['L3'] = df['L3'].apply(checkempty)
df[['W1', 'L1', 'W2', 'L2', 'W3', 'L3', 'W4', 'L4', 'W5', 'L5']] = df[['W1', 'L1', 'W2', 'L2', 'W3', 'L3', 'W4', 'L4', 'W5', 'L5']].astype(float).astype(int)

print("Processando informações dos jogadores e partidas...")

# Reorganize data into a standardized player 1 vs player 2 format
# alternating between winner and loser to avoid bias in the data
df['Player_1'] = df.apply(lambda row: row['Winner'] if row['ind'] == 0 else row['Loser'], axis = 1)
df['Player_2'] = df.apply(lambda row: row['Winner'] if row['ind'] == 1 else row['Loser'], axis = 1)
df['Rank_1'] = df.apply(lambda row: row['WRank'] if row['ind'] == 0 else row['LRank'], axis = 1)
df['Rank_2'] = df.apply(lambda row: row['WRank'] if row['ind'] == 1 else row['LRank'], axis = 1)
df['Pts_1'] = df.apply(lambda row: row['WPts'] if row['ind'] == 0 else row['LPts'], axis = 1)
df['Pts_2'] = df.apply(lambda row: row['WPts'] if row['ind'] == 1 else row['LPts'], axis = 1)
df['Odd_1'] = df.apply(lambda row: row['B365W'] if row['ind'] == 0 else row['B365L'], axis = 1)
df['Odd_2'] = df.apply(lambda row: row['B365W'] if row['ind'] == 1 else row['B365L'], axis = 1)

# Function to format the match score based on the index
def score(df):
    """
    Formats the match score as a string
    Args:
        df: DataFrame row containing match data
    Returns:
        Formatted string with the score of each set
    """
    if df['ind'] == 0:
        return str(df['W1']) + '-' + str(df['L1']) + ' ' + str(df['W2']) + '-' + str(df['L2']) + ' ' + str(df['W3']) + '-' + str(df['L3']) +\
 ' ' + str(df['W4']) + '-' + str(df['L4']) + ' ' + str(df['W5']) + '-' + str(df['L5']) + ' '
    return str(df['L1']) + '-' + str(df['W1']) + ' ' + str(df['L2']) + '-' + str(df['W2']) + ' ' + str(df['L3']) + '-' + str(df['W3']) +\
 ' ' + str(df['L4']) + '-' + str(df['W4']) + ' ' + str(df['L5']) + '-' + str(df['W5']) + ' '

# Apply the score function and clean the formatting
df['Score'] = df.apply(lambda row: score(row).replace('0-0', ''), axis = 1)
df['Score'] = df['Score'].apply(lambda x: x.strip())

# Function to handle "NR" (Not Ranked) rankings
def check(value):
    """
    Converts "NR" (Not Ranked) values to -1
    Args:
        value: Value to be checked
    Returns:
        -1 if the value is "NR", otherwise returns the original value
    """
    if isinstance(value, str) and value == 'NR':
        return -1
    return value

print("Finalizando e preparando os dados para salvar...")

# Create a new DataFrame with only the relevant columns
new_df = df[['Tournament', 'Date', 'Series', 'Court', 'Surface', 'Round', 'Best of', 'Player_1', 'Player_2',
             'Winner', 'Rank_1', 'Rank_2', 'Pts_1', 'Pts_2', 'Odd_1', 'Odd_2', 'Score']].copy()

# Convert the date column to datetime format
new_df['Date'] = pd.to_datetime(new_df['Date'], format='%Y-%m-%d', errors='coerce')
new_df = new_df.fillna(-1)

# Apply the check function to handle "NR" values and convert to integers
for col in ['Best of', 'Rank_1', 'Rank_2', 'Pts_1', 'Pts_2']:
    new_df[col] = new_df[col].apply(check)
    new_df[col] = new_df[col].astype(float).astype(int)

# Suppress specific openpyxl warnings about unknown extensions
warnings.filterwarnings("ignore", message="Unknown extension is not supported and will be removed", 
                       category=UserWarning, module="openpyxl")

# Save the processed DataFrame to a CSV file
new_df.to_csv('atp_tennis.csv', index=False)
print("\n✅ Processamento completo! Arquivo 'atp_tennis.csv' foi criado com sucesso.")
print(f"Total de partidas processadas: {len(new_df)}")