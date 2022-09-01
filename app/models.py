from app import db
#from app import login
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

class User(UserMixin, db.Model): #User table

  id = db.Column(db.Integer, primary_key=True) # Each user has only one unique id;
  email = db.Column(db.String(120), index=True, unique=True) 
  password_hash = db.Column(db.String(128))

class Four_Sem_SP(db.Model):
  Y1S1_1 = db.Column(db.String(10)),
  Y1S1_2 = db.Column(db.String(10)),
  Y1S1_3 = db.Column(db.String(10)),
  Y1S1_4 = db.Column(db.String(10)),
  Y1S1_5 = db.Column(db.String(10)),

  Y1S2_1 = db.Column(db.String(10)),
  Y1S2_2 = db.Column(db.String(10)),
  Y1S2_3 = db.Column(db.String(10)),
  Y1S2_4 = db.Column(db.String(10)),
  Y1S2_5 = db.Column(db.String(10)),
  
  Y2S1_1 = db.Column(db.String(10)),
  Y2S1_2 = db.Column(db.String(10)),
  Y2S1_3 = db.Column(db.String(10)),
  Y2S1_4 = db.Column(db.String(10)),
  Y2S1_5 = db.Column(db.String(10)),

  Y2S2_1 = db.Column(db.String(10)),
  Y2S2_2 = db.Column(db.String(10)),
  Y2S2_3 = db.Column(db.String(10)),
  Y2S2_4 = db.Column(db.String(10)),
  Y2S2_5 = db.Column(db.String(10))
  user_id = db.Column(db.Integer, db.ForeignKey('user.id')) # Reference to user id in user table

"""
@login.user_loader
def load_user(user_id):
  return User.query.get(user_id)

#Creating a connection cursor
cursor = mysql.connection.cursor()
 
#Executing SQL Statements
# Create user table
cursor.execute(''' CREATE TABLE User(
  UserID int NOT NULL,
  Email varchar(255) NOT NULL, 
  Password_hash varchar(255) NOT NULL,
  PRIMARY KEY (User_id,Email)
  ) ''')
 
# Create four semester studyplan table

cursor.execute(''' CREATE TABLE Four_Sem_SP(
  UserID int NOT NULL,
  Y1S1_1 varchar(8),
  Y1S1_2 varchar(8),
  Y1S1_3 varchar(8),
  Y1S1_4 varchar(8),
  Y1S1_5 varchar(8),
  Y1S1_6 varchar(8),
  Y1S2_1 varchar(8),
  Y1S2_2 varchar(8),
  Y1S2_3 varchar(8),
  Y1S2_4 varchar(8),
  Y1S2_5 varchar(8),
  Y1S2_6 varchar(8),
  Y2S1_1 varchar(8),
  Y2S1_2 varchar(8),
  Y2S1_3 varchar(8),
  Y2S1_4 varchar(8),
  Y2S1_5 varchar(8),
  Y2S1_6 varchar(8),
  Y2S2_1 varchar(8),
  Y2S2_2 varchar(8),
  Y2S2_3 varchar(8),
  Y2S2_4 varchar(8),
  Y2S2_5 varchar(8),
  Y2S2_6 varchar(8),
  FOREIGN KEY (UserID) REFERENCES User(UserID)
  ) ''')

# the add value statement: 
# INSERT INTO Four_Sem_SP(c1,c2,c3) Values(v1,v2,v3) If we do not specify column's name, the value
# will be added sequentially.
# Better to have a functon for each course in each semester, therefore, 24 functions will be required 

#Saving the Actions performed on the DB
mysql.connection.commit()
 
#Closing the cursor
cursor.close()
"""