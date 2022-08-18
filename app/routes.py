from app import app
from flask import render_template

@app.route('/')
@app.route('/index')
def index():
    #return "Hello world"
    return render_template('index.html', title='Home')



@app.route('/signUp', methods=['GET', 'POST'])
def signUp():
    return render_template('signUp.html')

# Login Page
@app.route('/login', methods=['GET', 'POST'])
def login():
    return render_template('login.html', title="Log In")

""" 
# logout the user and redirect to index page
@app.route('/logout')
def logout():
  logout_user()
  return redirect(url_for('index')) 
"""

# Studyplanner step 1
@app.route('/createstudyplan-courses', methods=['GET', 'POST'])
def createstudyplanstep1():
    return render_template('step1-createstudyplan.html', title="Create study plan")

# Studyplanner step 2
@app.route('/home', methods=['GET', 'POST'])
def home():
    return render_template('home.html', title="home")

#faq
@app.route('/faq', methods=['GET', 'POST'])
def faq():
    return render_template('faq.html', title="FAQ")



@app.errorhandler(404)
def page_not_found(e):
    return render_template('signUp.html'), 404
