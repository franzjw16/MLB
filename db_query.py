from mlb_model import Base, MLB
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import pandas as pd



engine = create_engine('sqlite:///mlb.db')
Base.metadata.bind = engine

DBSession = sessionmaker()
DBSession.bind = engine
session = DBSession()
# Make a query to find all Persons in the database
session.query(MLB).all()
print('Reading data from database...')
games = session.query(MLB).all()

df_1 = pd.DataFrame(columns = ['Date', 'Home_Team', 'Away_Team', 
                               'HT_Runs', 'HT_Hits', 'HT_Errors', 
                               'AT_Runs', 'AT_Hits', 'AT_Errors'])

for game in games:
    raw_data = {
    'Date': [game.date],
    'Home_Team': [game.home_team],
    'Away_Team': [game.away_team],
    'HT_Runs': [game.ht_runs],
    'HT_Hits': [game.ht_hits],
    'HT_Errors': [game.ht_errors],    
    'AT_Runs': [game.at_runs],
    'AT_Hits': [game.at_hits],
    'AT_Errors': [game.at_errors],}
    mlb_date_data1 = pd.DataFrame(raw_data, columns = ['Date', 'Home_Team', 'Away_Team', 
                                                       'HT_Runs', 'HT_Hits', 'HT_Errors', 
                                                       'AT_Runs', 'AT_Hits', 'AT_Errors'])
    # Append scraped test data to df1
    df_1 = df_1.append(mlb_date_data1)

print('Writing dataframe out to mlb_historial_game_results.csv')
df_1.to_csv('mlb_historial_game_results.csv', index=False)
#df = pd.DataFrame.from_records(games)
#
#print(df)

