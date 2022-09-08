from app import app
from flask import render_template, redirect, url_for, flash, request
from flask_login import current_user, login_user, logout_user, login_required
from app.forms import RegistrationForm, LoginForm
from .models import User, Four_Sem_SP
from . import db
from werkzeug.urls import url_parse


@app.route('/')
@app.route('/index', methods=['GET', 'POST'])
def index():
    return render_template('index.html', title='Home')

# Signup Page
@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if current_user.is_authenticated:
        return redirect(url_for('login'))
    form = RegistrationForm()
    if request.method == 'POST':
        if form.validate_on_submit():
            user = User(email=form.email.data, password=form.password.data)
            user.set_password(form.password.data)
            db.session.add(user) # Add latest registered user into the database model
            db.session.commit()
            return redirect(url_for('login'))
    return render_template('signup.html', title='Sign Up', form=form)

# Login Page
@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm() 
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid email or password')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            return redirect(url_for('index'))
        return redirect(next_page)
    return render_template('login.html', title="Log In", form=form)


# logout the user and redirect to index page
@app.route('/logout', methods=['GET', 'POST'])
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))


# Account Page
@app.route('/myaccount', methods=['GET', 'POST'])
def myaccount():
    #Get user account
    user=current_user.username
    #Check if user data exists

    #If true, get user data
    return render_template('myaccount.html', title="My Account")


# Studyplanner step 1
@app.route('/createstudyplan-courses', methods=['GET', 'POST'])
def createstudyplanstep1():
    return render_template('step1-createstudyplan.html', title="Create study plan")

# Studyplanner step 2
@app.route('/createstudyplan-units', methods=['GET', 'POST'])
def createstudyplanstep2():
    return render_template('step2-createstudyplan.html', title="Create study plan")

# Download PDF
@app.route('/pdf', methods=['GET', 'POST'])
def download():
    return render_template('get_pdf.html', title="PDF")

# FAQ Page
@app.route('/faq', methods=['GET', 'POST'])
def faq():
    return render_template('faq.html', title="FAQ")

# 404 Page
@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

if __name__ == '__main__':
    app.run(debug=True)