
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
 
from db_mlb_model import Base, MLB
 
engine = create_engine('sqlite:///mlb.db')
# Bind the engine to the metadata of the Base class so that the
# declaratives can be accessed through a DBSession instance
Base.metadata.bind = engine
 
DBSession = sessionmaker(bind=engine)
# A DBSession() instance establishes all conversations with the database
# and represents a "staging zone" for all the objects loaded into the
# database session object. Any change made against the objects in the
# session won't be persisted into the database until you call
# session.commit(). If you're not happy about the changes, you can
# revert all of them back to the last commit by calling
# session.rollback()
session = DBSession()
 
# Insert 'dummy/test' Record
new_record = MLB(date='2019-03-11', home_team='team1', away_team='team2', home_team_runs=4, away_team_runs=5)
session.add(new_record)
session.commit()
 
