# -*- coding: utf-8 -*-
"""
Created on Wed Mar 13 10:19:22 2019

@author: Franz
"""

from mlb_model import Base, MLB
from sqlalchemy import create_engine
engine = create_engine('sqlite:///mlb.db')
Base.metadata.bind = engine
from sqlalchemy.orm import sessionmaker
DBSession = sessionmaker()
DBSession.bind = engine
session = DBSession()

session.query(MLB).delete()
session.commit()
    
print('All records deleted in MLB database.')