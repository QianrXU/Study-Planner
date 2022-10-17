# The database test logic followed the 
# https://www.softwaretestinghelp.com/database-testing-process/#1_Transactions
# to ensure data integrity and the CRUD operations can be applied to the database

# Database Schema Testing
# Print out all the attributes of the tables

import sqlalchemy as db
from datetime import datetime

# Set up enviroment
engine = db.create_engine('sqlite:///app/db.sqlite')
connection = engine.connect()
metadata = db.MetaData() 
user = db.Table('User', metadata, autoload=True, autoload_with=engine) 
studyplan = db.Table('Four__Sem_SP', metadata, autoload=True, autoload_with=engine)


# Data creation test
created_tables = engine.table_names()
try:
  'user' in created_tables
  print('user table has been created')
except:
  print('user table has not been created')

try:
  'four__sem_SP' in created_tables
  print('studyplan table has been created')
except:
  print('studyplan table has not been created')


# Check out the Schema of User Table

user_table_schema = ['id', 'email', 'password_hash']
study_plan_schema = ['study_plan_id', 'Y1S1_1', 'Y1S1_2', 'Y1S1_3', 'Y1S1_4', 
'Y1S1_5', 'Y1S2_1', 'Y1S2_2', 'Y1S2_3', 'Y1S2_4', 'Y1S2_5', 'Y2S1_1', 'Y2S1_2', 
'Y2S1_3', 'Y2S1_4', 'Y2S1_5', 'Y2S2_1', 'Y2S2_2', 'Y2S2_3', 'Y2S2_4', 'Y2S2_5', 
'startYearSem', 'selectedCourse', 'selectedMajor', 'faculty', 'coursecode', 'user_id', 'date_updated']

try:
  user_table_schema == user.columns.keys()
  print('Schema of User Table is correct')
except:
  print('Schema of User Table is incorrect, codes need to be reviewed')

try:
  study_plan_schema == studyplan.columns.keys()
  print('Schema of Four Semester Study Plan Table is correct')
except:
  print('Schema of Four Semester Study Plan Table is incorrect, codes need to be reviewed')
  

# Database Transactions Testing

# Add data for user table
addQuery = db.insert(user).values(id=1, email='1234@mail.com', password='123456') 
try:
  addData = connection.execute(addQuery)
  print("Able to add data to User table")

except:
  print("Unable to add data to User table")

# We cannot add data through database in the user table for this case because all the password are encrypted
# and recorded in the table as password_hash instead of password

# Delete data from user table
deleteQuery = db.delete(user)
deleteQuery = deleteQuery.where(user.columns.id == 2)

try:
  deleteData = connection.execute(deleteQuery)
  print('Able to delete data from User table :)')
except:
  print("Unable to add data from User table")


# Add data for Four Semester Study Plan table
addQuery_SP = db.insert(studyplan).values(study_plan_id=100, Y1S1_1='STAT2402 Analysis of Observations',Y1S1_2='CITS4009 Computational Data Analysis',
startYearSem='Semester 2, 2023',selectedCourse='Master of Data Science',faculty='Physics, Mathematics and Computing',coursecode='62530',user_id=1,date_updated=datetime(2022, 3, 3, 10, 10, 10)) 

try:
  addData = connection.execute(addQuery_SP)
  print("Able to add data to Four Semester Study Plan table :)")

except:
  print("Unable to add data to Four Semester Study Plan table")


# Delete data from Four Semester Study Plan table
deleteQuery_SP = db.delete(studyplan)
deleteQuery_SP = deleteQuery_SP.where(studyplan.columns.study_plan_id == 100)

try:
  deleteData = connection.execute(deleteQuery_SP)
  print('Able to delete data from Four Semester Study Plan table :)')
except:
  print("Unable to add data from Four Semester Study Plan table")

