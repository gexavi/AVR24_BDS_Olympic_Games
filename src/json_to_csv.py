# Import des librairies
import pandas as pd
import json
from pandas import json_normalize

# Chargement du fichier json
with open('data.json', 'r') as file:
    data = json.load(file)

# Le json est une suite de dictionnaires imbriques. Nous allons normaliser les donnees
# Initialisation d'une liste pour stocker les DataFrames temporaires
dfs = []

# Extraire le nom de la competition
competition_name = data['data']['getCalendarCompetitionResults']['competition']['name']

# Parcourir chaque titre d'evenement et chaque evenement
for event in data['data']['getCalendarCompetitionResults']['eventTitles']:
    for race_event in event['events']:
        for race in race_event['races']:
            # Normaliser les donnees de resultats de la course
            df = json_normalize(race, 'results', errors='ignore')
            # Ajouter des informations sur l'evenement et la course
            df['event'] = race_event['event']
            df['gender'] = race_event['gender']
            df['race_type'] = race['race']
            df['race_number'] = race['raceNumber']
            df['race_date'] = race['date']
            df['wind'] = race['wind']
            df['competition_name'] = competition_name
            dfs.append(df)

# Concatener tous les DataFrames en un seul
final_df = pd.concat(dfs, ignore_index=True)

# Renommer les colonnes pour plus de clarte
final_df.rename(columns={
    'competitor.name': 'Name',
    'competitor.nationality': 'Nationality',
    'competitor.birthDate': 'Birthdate',
    'mark': 'Mark',
    'place': 'Place',
    'race_type': 'Race Type',
    'race_date': 'Race Date'
}, inplace=True)

# Sauvegarder le DataFrame en CSV
final_df.to_csv('100m.csv', index=False)