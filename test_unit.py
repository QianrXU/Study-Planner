
import pytest
import unittest,os
from app import app, db
from app.models import User
from app.forms import RegistrationForm, LoginForm

class UserModelCase(unittest.TestCase):

  def setUp(self):
    basedir = os.path.abspath(os.path.dirname(__file__))
    app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///'+os.path.join(basedir,'test.db')
    self.app = app.test_client() # create a virtual test enviroment
    # Create all tables 
    db.create_all()
    # create 3 users as test cases
    user1 = User(email='123@mail.com', password='testing1')
    user2 = User(email='456@mail.com', password='testing2')
    user3 = User(email='789@mail.com', password='testing3')
    db.session.add(user1)
    db.session.add(user2)
    db.session.add(user3)
    db.session.commit()
    self.assertEquals(app.debug, False)

  def tearDown(self):
    # remove all the db data so the test can be reusable
    db.session.remove() 
    db.drop_all()
  
  # __init__() test including:
  # Email check(Wether can login with registered/non-registered emails)
  # Password check(registered email address login attempts with right/wrong passwords)

  def test_password_hashing(self):
    user1 = User.query.filter_by(email='123@mail.com')
    user1.set_password('testing1')
    self.assertFalse(user1.check_password('nonsense'))
    self.assertTrue(user1.check_password('testing1'))

  def register(self,username,email,password,confirm):
    return self.app.post('signup/', 
    data=dict(username=username,email=email, password=password, confirm=confirm),
    follow_redirects=True)

  # user registration form displays test
  # Required Ancy to do

  def test_valid_user_registration(self):
    self.app.get('/signup', follow_redirects=True)
    response = self.register('capstone@mail.com', 'Teamwork', 'Teamwork')
    self.assertIn(b'', response.data)

  def test_registration_different_passwords(self):
    response = self.register('test1@mail.com', 'ILoveTeamwork', 'IHateTeamwork')
    self.assertIn(b'Field must be equal to password.', response.data)

  def test_registration_duplicate_email(self):
    response = self.register('test2@mail.com', 'ILoveTeamwork', 'ILoveTeamwork')
    self.assertEqual(response.status_code, 200)
    response = self.register('test2@mail.com', 'IHateTeamwork', 'IHateTeamwork')
    self.assertIn(b'This email has already registered, please pick a different one', response.data)
    
  def login(self, username, password):
    return self.app.post('/login',
    data=dict(username=username, password=password),
    follow_redirects=True)

if __name__ == "__main__":
    unittest.main()

  
  