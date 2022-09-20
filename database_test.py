# Database Schema Testing
# Print out all the attributes of the tables

import sqlalchemy as db
import pandas as pd

engine = db.create_engine('sqlite:///app/db.sqlite')
connection = engine.connect()
metadata = db.MetaData() 
user = db.Table('User', metadata, autoload=True, autoload_with=engine) 

# Check out the Schema of User Table
print(user.columns.keys())
print(repr(metadata.tables['User']))



###### Unable to test the Four_Sem_SP table for now (Will be tested in Sprint 3) ####

# Studyplan table will not be accessed so far since we do not have any data, so
# this table hasn't been created yet. 
# studyplan = db.Table('Four_Sem_SP', metadata, autoload=True, autoload_with=engine)




# The database test followed the 
# https://www.softwaretestinghelp.com/database-testing-process/#1_Transactions

# Database are tested to ensure (1) Data Mapping (2) ACID Properties Validation and (3) Data Integrity

# Transaction Testing