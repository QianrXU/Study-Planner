from app import app
from flask import render_template, redirect, url_for
from flask_login import current_user, login_user, logout_user, login_required

@app.route('/')
@app.route('/index', methods=['GET', 'POST'])
def index():
    return render_template('index.html', title='Home')


<<<<<<< HEAD
@app.route('/signup', methods=['GET', 'POST'])
def signup():
    return render_template('signUp.html', title='Sign Up')



=======
>>>>>>> main
# Login Page
@app.route('/login', methods=['GET', 'POST'])
def login():
    return render_template('login.html', title="Log In")

"""
# logout the user and redirect to index page
@app.route('/logout', methods=['GET', 'POST'])
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))
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

@app.route('/faq', methods=['GET', 'POST'])
def faq():
    return render_template('faq.html', title='FAQ')


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

if __name__ == '__main__':
    app.run(debug=True)
