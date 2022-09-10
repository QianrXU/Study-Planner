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
def account():
    return render_template('myaccount.html', title="My Account")

import pandas as pd
import json
import os
import re
from flask import request
from flask import jsonify
from werkzeug.wrappers import Request, Response

# Studyplanner step 1
@app.route('/createstudyplan-courses', methods=['GET', 'POST'])
def createstudyplanstep1():

    # WILL NEED TO FILTER BY YEAR. 
    # PROBABLY BEST TO REMOVE UNWANTED YEARS FROM USER STANDPOINT DIRECTLY FROM CSV? /C

    # declare global variables
    global selectedCourse
    global faculty
    global coursecode

    # save csv file into dataframe
    targetcsv = os.path.join(app.static_folder, 'Json-export-bite.csv')
    df = pd.read_csv(targetcsv, sep=",")

    # process ListMajors column
    majors = df['ListMajors'].dropna().values.tolist() # create dataframe of listmajors column
    pattern = r'[(\d)\'<b]+'
    majors = ' '.join(str(e) for e in majors)
    majors = re.split(pattern, majors)
    majors = ' '.join(str(e) for e in majors)
    newpattern = r'[\']+'
    majors = re.split(newpattern, majors)
    majors = ' '.join(str(e) for e in majors)
    majors = majors.split(" r>")

    # TO DO 1
    # need to figure out how to filter out degrees that are actually
    # majors, e.g., Accounting and Business Law are majors (Bachelor of Commerce) 
    # should not be in Course selection (will appear in majors too).
    # Logic: If degree exists in major, pop item from degree dicitonary

    # degrees
    degrees_withID = dict(zip(df.Title, df.CourseID))
    degrees_withFaculty = dict(zip(df.Title, df.Faculty))
    degrees = sorted(degrees_withID.keys())
    faculty = dict(zip(df.Faculty, df.CourseID))

    if request.method == 'POST':
        try:
            selectedCourse = request.form.get('name') # saves selected course into variable
            for key, value in degrees_withID.items(): # iterates through values to find course code
                if selectedCourse == key:
                    coursecode=value
            for key, value in degrees_withFaculty.items(): # iterates through values to find course code
                if selectedCourse == key:
                    faculty=value
        except:
            return render_template('404.html'), 404
        return ('', 204) # indicates post response has been done successfully 
    
    return render_template('step1-createstudyplan.html',
            degrees_withID=degrees_withID,
            degrees=degrees, 
            majors=majors,
            #d=d,
            faculty=faculty,
            title="Create study plan")

# Studyplanner step 2
@app.route('/createstudyplan-units', methods=['GET', 'POST'])
def createstudyplanstep2():
    try:
        global selectedCourse 
        global faculty
        global coursecode
        return render_template('step2-createstudyplan.html', 
            selectedCourse=selectedCourse, 
            faculty=faculty,
            coursecode=coursecode,
            title="Create study plan")
    except:
        return render_template('404.html'), 404

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