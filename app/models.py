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

  startYearSem = db.Column(db.String(200), nullable=False)
  selectedCourse = db.Column(db.String(200), nullable=False)
  selectedMajor = db.Column(db.String(200))
  faculty = db.Column(db.String(200), nullable=False)
  coursecode = db.Column(db.String(200), nullable=False)
  user_id = db.Column(db.Integer, db.ForeignKey('user.id')) # Reference to user id in user table
  date_updated=db.Column(db.DATETIME(timezone=True), nullable=False, default=func.now())

user= User('test@mail.com', 'password')
studyPlan= Four_Sem_SP(Y1S1_1 = 'CITS4401 Software Requirements and Design',
  Y1S1_2 = 'CITS4407 Open Source Tools and Scripting',
  Y1S1_3 = 'CITS5501 Software Testing and Quality Assurance',
  Y1S1_4 = 'CITS5505 Agile Web Development',
  Y1S1_5 = '',

  Y1S2_1 = 'CITS5503 Cloud Computing',
  Y1S2_2 = 'CITS5506 The Internet of Things',
  Y1S2_3 = 'GENG5505 Project Management and Engineering Practice',
  Y1S2_4 = 'CITS4009 Computational Data Analysis',
  Y1S2_5 = '',
  
  Y2S1_1 = 'CITS4012 Natural Language Processing',
  Y2S1_2 = 'CITS4404 Artificial Intelligence and Adaptive Systems',
  Y2S1_3 = 'CITS5504 Data Warehousing',
  Y2S1_4 = 'CITS5508 Machine Learning',
  Y2S1_5 = '',

  Y2S2_1 = 'CITS4403 Computational Modelling',
  Y2S2_2 = 'CITS4009 Computational Data Analysis',
  Y2S2_3 = 'CITS5507 High Performance Computing',
  Y2S2_4 = 'CITS5206 Information Technology Capstone Project',
  Y2S2_5 = '',

  startYearSem = 'Semester 1, 2023',
  selectedCourse = 'Master of Information Technology',
  selectedMajor = '',
  faculty = 'Physics, Mathematics and Computing',
  coursecode = '62510',
  user_id = 1)


db.drop_all()
db.create_all()
db.session.add(user)
db.session.add(studyPlan)
db.session.commit()


