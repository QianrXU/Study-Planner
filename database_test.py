# The database test logic followed the 
# https://www.softwaretestinghelp.com/database-testing-process/#1_Transactions
# to ensure data integrity and the CRUD operations can be applied to the database

# Database Schema Testing
# Print out all the attributes of the tables

import sqlalchemy as db
import pandas as pd

engine = db.create_engine('sqlite:///app/db.sqlite')
connection = engine.connect()
metadata = db.MetaData() 
user = db.Table('User', metadata, autoload=True, autoload_with=engine) 
studyplan = db.Table('Four_Sem_SP', metadata, autoload=True, autoload_with=engine)

# Check out the Schema of User Table
print(user.columns.keys())
print(repr(metadata.tables['User']))

# Print out the data in the current user table
results = connection.execute(db.select([user])).fetchall() 
df = pd.DataFrame(results) # create dataframe
df.columns = results[0].keys() # set up the columns name
print(df)


# Database Transactions Testing

# Add data
addQuery = db.insert(user).values(id=1, email='1234@mail.com', password='123456') 
try:
  addData = connection.execute(addQuery)
except:
  print("Unable to add data")

# We cannot add data through database in the user table for this case because all the password are encrypted
# and recorded in the table as password_hash instead of password

# Delete data
deleteQuery = db.delete(user)
deleteQuery = deleteQuery.where(user.columns.id == 2)

try:
  deleteData = connection.execute(deleteQuery)
  print('Able to delete :)')
except:
  print("Unable to add data")


###### Unable to test the Four_Sem_SP table for now (Will be tested in Sprint 3) ####
##### Trigger Testing for database will be tested in Sprint 3 too #####

# Studyplan table will not be accessed so far since we do not have any data, so
# this table hasn't been created yet. 
# studyplan = db.Table('Four_Sem_SP', metadata, autoload=True, autoload_with=engine)