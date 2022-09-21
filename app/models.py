from app import db
from sqlalchemy.sql import func
from app import login
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

@login.user_loader
def load_user(id):
  return User.query.get(id)

class User(db.Model,UserMixin): #User table

  id = db.Column(db.Integer, primary_key=True) # Each user has only one unique id;
  email = db.Column(db.String(120), index=True, unique=True) 
  password = db.Column(db.String(128))
  password_hash = db.Column(db.String(128))


  def __init__(self, email, password):
    self.email = email
    self.set_password(password)

  def __repr__(self):
    return '<User %r>' % self.email

  def set_password(self, password):
    self.password_hash = generate_password_hash(password)

  def check_password(self, password):
    return check_password_hash(self.password_hash, password)

  def is_authenticated(self):
    return True

class Four_Sem_SP(db.Model):
  study_plan_id = db.Column(db.Integer, primary_key=True)

  Y1S1_1 = db.Column(db.String(200))
  Y1S1_2 = db.Column(db.String(200))
  Y1S1_3 = db.Column(db.String(200))
  Y1S1_4 = db.Column(db.String(200))
  Y1S1_5 = db.Column(db.String(200))

  Y1S2_1 = db.Column(db.String(200))
  Y1S2_2 = db.Column(db.String(200))
  Y1S2_3 = db.Column(db.String(200))
  Y1S2_4 = db.Column(db.String(200))
  Y1S2_5 = db.Column(db.String(200))
  
  Y2S1_1 = db.Column(db.String(200))
  Y2S1_2 = db.Column(db.String(200))
  Y2S1_3 = db.Column(db.String(200))
  Y2S1_4 = db.Column(db.String(200))
  Y2S1_5 = db.Column(db.String(200))

  Y2S2_1 = db.Column(db.String(200))
  Y2S2_2 = db.Column(db.String(200))
  Y2S2_3 = db.Column(db.String(200))
  Y2S2_4 = db.Column(db.String(200))
  Y2S2_5 = db.Column(db.String(200))

  selectedCourse = db.Column(db.String(200))
  selectedMajor = db.Column(db.String(200))
  faculty = db.Column(db.String(200))
  coursecode = db.Column(db.String(200))
  user_id = db.Column(db.Integer, db.ForeignKey('user.id')) # Reference to user id in user table
  date_updated=db.Column(db.DATETIME(timezone=True), nullable=False, default=func.now())

