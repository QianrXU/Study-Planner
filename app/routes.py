from app import app
from flask import render_template, redirect, url_for, flash, request
from flask_login import current_user, login_user, logout_user, login_required
from app.forms import RegistrationForm, LoginForm
from .models import User, Four_Sem_SP
from . import db
from werkzeug.urls import url_parse
import pandas as pd
import os
import re
import json


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



# Studyplanner step 1
@app.route('/createstudyplan-courses', methods=['GET', 'POST'])
def createstudyplanSelectCourse():

    # WILL NEED TO FILTER BY YEAR. 
    # PROBABLY BEST TO REMOVE UNWANTED YEARS FROM USER STANDPOINT DIRECTLY FROM CSV, 
    # OTHERWISE THEY'D HAVE TO GO INTO THE SOURCE CODE TO CHANGE IT? /C

    # declare global variables
    global selectedCourse
    global faculty
    global coursecode
    global getMajorValues
    global getUnitValues

    # save csv file into dataframe
    targetcsv = os.path.join(app.static_folder, 'Json-export-bite.csv')
    df = pd.read_csv(targetcsv, sep=",")

    # Dataframe generation
    degrees = df[~df.CourseID.str.startswith('MJD')] # remove any course IDs that start with MJD (i.e., majors). This is the column that the degrees selection dropdown will choose its values from.
    degrees = dict(zip(degrees.Title, degrees.CourseID))
    degrees = sorted(degrees.keys())

    degrees_withID = dict(zip(df.Title, df.CourseID))
    degrees_withFaculty = dict(zip(df.Title, df.Faculty))
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
            getMajorValues = df[df.Title.eq(selectedCourse)] # get dataframe for selected course, to be used in Major 
            getUnitValues = df[df.Title.eq(selectedCourse)] #  get dataframe for selected course, to be used in Units

        except:
            return render_template('404.html'), 404
        return ('', 204) # indicates post response has been done successfully
    
    return render_template('1course-createstudyplan.html',
            degrees_withID=degrees_withID,
            degrees=degrees, 
            faculty=faculty,
            title="Create study plan")

# Download PDF
@app.route('/createstudyplan-majors', methods=['GET', 'POST'])
def createstudyplanSelectMajor():
    try:
        global getMajorValues

        # process ListMajors column
        newmajors = getMajorValues['ListMajors'].dropna().values.tolist() # create dataframe of listmajors column
        pattern = r'[(\d)\'<b]+'
        newmajors = ' '.join(str(e) for e in newmajors)
        newmajors = re.split(pattern, newmajors)
        newmajors = ' '.join(str(e) for e in newmajors)
        newpattern = r'[\']+'
        newmajors = re.split(newpattern, newmajors)
        newmajors = ' '.join(str(e) for e in newmajors)
        newmajors = newmajors.split(" r>")

        return render_template('2major-createstudyplan.html',
            newmajors=newmajors,
            getMajorValues=getMajorValues,
            title="Create study plan")
    except:
        return render_template('404.html'), 404

# Studyplanner step 2
@app.route('/createstudyplan-units', methods=['GET', 'POST'])
def createstudyplanSelectUnits():
    try:
        global selectedCourse 
        global faculty
        global coursecode
        global getUnitValues

        # process units based on course selection
        unitValues = getUnitValues['Structure'].dropna() # create dataframe of listmajors column
        unitValues = [str(x) for x in unitValues][0] # convert to string
        unitValues = unitValues[1:-1]
        unitValues = json.loads(unitValues) # json file
        test = json.dumps(unitValues)



        return render_template('3grid-createstudyplan.html', 
            unitValues=unitValues,
            selectedCourse=selectedCourse, 
            test=test,
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