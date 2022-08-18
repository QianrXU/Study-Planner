from app import app
from flask import render_template

@app.route('/')
@app.route('/index', methods=['GET', 'POST'])
def index():
    #return "Hello world"
    return render_template('index.html', title='Home')


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
@app.route('/createstudyplan-units', methods=['GET', 'POST'])
def createstudyplanstep2():
    return render_template('step2-createstudyplan.html', title="Create study plan")

# FAQ
@app.route('/faq', methods=['GET', 'POST'])
def faq():
    return render_template('faq.html', title="FAQ")

    
@app.route('/signup', methods=['GET', 'POST'])
def signup():
    return render_template('signup.html', title='Sign up')

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404
