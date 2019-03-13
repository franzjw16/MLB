
import os
import sys
from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine
 
Base = declarative_base()
 
class MLB(Base):
    __tablename__ = 'mlb_results_history'
    # Here we define columns for the table mlb_results_history
    # Notice that each column is also a normal Python instance attribute.
    id = Column(Integer, primary_key=True)
    date = Column(String(15), nullable=False)
    home_team = Column(String(30))
    away_team = Column(String(30))
    ht_runs = Column(String(3))
    ht_hits = Column(String(3))
    ht_errors = Column(String(3))
    at_runs = Column(String(3))
    at_hits = Column(String(3))
    at_errors = Column(String(3))
    
    def __repr__(self):
        return f'''<ID {self.id}, Date {self.date}, Home Team {self.home_team}, Away Team {self.away_team}, 
HT Runs {self.ht_runs}, HT Hits {self.ht_hits}, HT Errors {self.ht_errors},
AT Runs {self.at_runs}, AT Runs {self.at_hits}, AT Runs {self.at_errors}>\n'''
 
# Create an engine that stores data in the local directory's
engine = create_engine('sqlite:///mlb.db')
 
# Create all tables in the engine. This is equivalent to "Create Table"
# statements in raw SQL.
Base.metadata.create_all(engine)

