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


# STUDY PLANNER - SELECT COURSE
@app.route('/createstudyplan-courses', methods=['GET', 'POST'])
def createstudyplanSelectCourse():
    # declare global variables
    global selectedCourse
    global faculty
    global coursecode
    global getMajorValues
    global getUnitValues
    global selectedMajor

    # save csv file into dataframe
    targetcsv = os.path.join(app.static_folder, 'Json-export.csv')
    df = pd.read_csv(targetcsv, sep=",")
    selectedYear = 2022 # Filters by year. Change value to other year if wanted/needed.
    df = df[df.Year.eq(selectedYear)]
    df = df[df['Structure'].notna()] # Removes all options from dataframe where Structure cell is empty

    # Dataframe generation
    degrees = df[~df.CourseID.str.startswith('MJD')] # remove any course IDs that start with MJD (i.e., majors). This is the column that the degrees selection dropdown will choose its values from.
    degrees = dict(zip(degrees.Title, degrees.CourseID))
    degrees = sorted(degrees.keys())

    degrees_withID = dict(zip(df.Title, df.CourseID))
    degrees_withFaculty = dict(zip(df.Title, df.Faculty))
    faculty = dict(zip(df.Faculty, df.CourseID))

    # TO DO - Need to check if selected degree ListMajors and ListMajors2 empty, 
    # if empty give selected major ..
    selectedMajor = "No major or specification available"

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

# STUDY PLANNER - SELECT MAJOR
@app.route('/createstudyplan-majors', methods=['GET', 'POST'])
def createstudyplanSelectMajor():
    try:
        global selectedMajor
        global getMajorValues

        # process ListMajors column
        majors = getMajorValues['ListMajors'].dropna().values.tolist() # create dataframe of ListMajors column
        #majors2 = getMajorValues['ListMajors2'].dropna().values.tolist() # create dataframe of ListMajors2 column - SOMETIMES MAJORS ARE LISTED IN THIS COLUMN, WE'LL NEED TO RUN SOME CHECKS TO SEE WHICH ONE IS ACCURATE FOR SELECTED COURSE
        pattern = r'[(\d)\'<b]+'
        majors = ' '.join(str(e) for e in majors)
        majors = re.split(pattern, majors)
        majors = ' '.join(str(e) for e in majors)
        newpattern = r'[\']+'
        majors = re.split(newpattern, majors)
        majors = ' '.join(str(e) for e in majors)
        majors = majors.split(" r>")

        # retrieve selected major
        if request.method == 'POST':
            try:
                selectedMajor = request.form.get('name') # saves selected major into variable
            except:
                return render_template('404.html'), 404
            return ('', 204) # indicates post response has been done successfully

        return render_template('2major-createstudyplan.html',
            majors=majors,
            getMajorValues=getMajorValues,
            title="Create study plan")
    except:
        return render_template('404.html'), 404

# STUDY PLANNER - SELECT UNITS
@app.route('/createstudyplan-units', methods=['GET', 'POST'])
def createstudyplanSelectUnits():
    try:
        global selectedCourse 
        global selectedMajor
        global faculty
        global coursecode
        global getUnitValues

        # process units based on course selection
        unitValues = getUnitValues['Structure'].dropna() # create dataframe of listmajors column
        unitValues = [str(x) for x in unitValues][0] # convert to string
        unitValues = unitValues[1:-1]
        unitValues = json.loads(unitValues) # json file

        #courseInfo = unitValues['introduction'] #retrieve information from introduction (sometimes does not exists, may need to deal with somehow?)
        
        levelsSpecials = unitValues['levelsSpecials'] #retrieve levelsSpecials and place it in List
        lengthLS = len(levelsSpecials)
        typeNames = [] # extract all typesnames from 'Structure'
        for i in range(lengthLS): # loop through list
            for key, val in levelsSpecials[i].items():
                if key == 'unitTypes':
                    typeNames.append(val)

        units1 = []
        units2 = []
        units3 = []
        units4 = []
        units5 = []
        units6 = []
        units7 = []
        units8 = []

        # If someone knows how to create new variables in a loop, otherwise this solution works
        # for every unit role/type (conversion, option, core, etc) within the selected course, save them to a separate list
        try: 
            type1 = typeNames[0]
            lengthtype1 = len(type1)
            type1units = []
            for i in range(lengthtype1): # loop through list
                for key, val in type1[i].items():
                    if key == 'typeName': # e.g., conversion, core, option, etc.
                        units1.append(val)
                    if key == 'typeInto': # if there is any typeInto field, include this
                        units1.append(val)
                    type1units = val # creates list with dictionary of units in type1 group
            lengthtype1 = len(type1units)
            for i in range(lengthtype1): # loop through list and take the following from Structure
                for key, val in type1units[i].items():
                    if key == 'unitCode':
                        units1.append(val)
                    if key == 'unitTitle':
                        units1.append(val)
                    if key == 'unitPoints':
                        units1.append(val)
                    if key == 'unitURL':
                        units1.append(val)
        except: type1 = "No Type 1"

        try: 
            type2 = typeNames[1]
            lengthtype2 = len(type2)
            type2units = []
            for i in range(lengthtype2): # loop through list
                for key, val in type2[i].items():
                    if key == 'typeName': # e.g., conversion, core, option, etc.
                        units2.append(val)
                    if key == 'typeInto': # if there is any typeInto field, include this
                        units2.append(val) 
                    type2units = val # creates list with dictionary of units in type1 group
            lengthtype2 = len(type2units)
            for i in range(lengthtype2): # loop through list and take the following from Structure
                for key, val in type2units[i].items():
                    if key == 'unitCode':
                        units2.append(val)
                    if key == 'unitTitle':
                        units2.append(val)
                    if key == 'unitPoints':
                        units2.append(val)
                    if key == 'unitURL':
                        units2.append(val)
        except: type2 = "No Type 2"

        try: 
            type3 = typeNames[2]
            lengthtype3 = len(type3)
            type3units = []
            for i in range(lengthtype3): # loop through list
                for key, val in type3[i].items():
                    if key == 'typeName': # e.g., conversion, core, option, etc.
                        units3.append(val)
                    if key == 'typeInto': # if there is any typeInto field, include this
                        units3.append(val) 
                    type3units = val # creates list with dictionary of units in type1 group
            lengthtype3 = len(type3units)
            for i in range(lengthtype3): # loop through list and take the following from Structure
                for key, val in type3units[i].items():
                    if key == 'unitCode':
                        units3.append(val)
                    if key == 'unitTitle':
                        units3.append(val)
                    if key == 'unitPoints':
                        units3.append(val)
                    if key == 'unitURL':
                        units3.append(val)
        except: type3 = "No Type 3"

        try: 
            type4 = typeNames[3]
            lengthtype4 = len(type4)
            type4units = []
            for i in range(lengthtype4): # loop through list
                for key, val in type4[i].items():
                    if key == 'typeName': # e.g., conversion, core, option, etc.
                        units4.append(val)
                    if key == 'typeInto': # if there is any typeInto field, include this
                        units4.append(val) 
                    type4units = val # creates list with dictionary of units in type1 group
            lengthtype4 = len(type4units)
            for i in range(lengthtype4): # loop through list and take the following from Structure
                for key, val in type4units[i].items():
                    if key == 'unitCode':
                        units4.append(val)
                    if key == 'unitTitle':
                        units4.append(val)
                    if key == 'unitPoints':
                        units4.append(val)
                    if key == 'unitURL':
                        units4.append(val)
        except: type4 = "No Type 4"
        
        try: 
            type5 = typeNames[4]
            lengthtype5 = len(type5)
            type5units = []
            for i in range(lengthtype5): # loop through list
                for key, val in type5[i].items():
                    if key == 'typeName': # e.g., conversion, core, option, etc.
                        units5.append(val)
                    if key == 'typeInto': # if there is any typeInto field, include this
                        units5.append(val) 
                    type5units = val # creates list with dictionary of units in type1 group
            lengthtype5 = len(type5units)
            for i in range(lengthtype5): # loop through list and take the following from Structure
                for key, val in type5units[i].items():
                    if key == 'unitCode':
                        units5.append(val)
                    if key == 'unitTitle':
                        units5.append(val)
                    if key == 'unitPoints':
                        units5.append(val)
                    if key == 'unitURL':
                        units5.append(val)
        except: type5 = "No Type 5"
        
        try: 
            type6 = typeNames[5]
            lengthtype6 = len(type6)
            type6units = []
            for i in range(lengthtype6): # loop through list
                for key, val in type6[i].items():
                    if key == 'typeName': # e.g., conversion, core, option, etc.
                        units6.append(val)
                    if key == 'typeInto': # if there is any typeInto field, include this
                        units6.append(val) 
                    type6units = val # creates list with dictionary of units in type1 group
            lengthtype6 = len(type6units)
            for i in range(lengthtype6): # loop through list and take the following from Structure
                for key, val in type6units[i].items():
                    if key == 'unitCode':
                        units6.append(val)
                    if key == 'unitTitle':
                        units6.append(val)
                    if key == 'unitPoints':
                        units6.append(val)
                    if key == 'unitURL':
                        units6.append(val)
        except: type6 = "No Type 6"

        try: 
            type7 = typeNames[6]
            lengthtype7 = len(type7)
            type7units = []
            for i in range(lengthtype7): # loop through list
                for key, val in type7[i].items():
                    if key == 'typeName': # e.g., conversion, core, option, etc.
                        units7.append(val)
                    if key == 'typeInto': # if there is any typeInto field, include this
                        units7.append(val) 
                    type7units = val # creates list with dictionary of units in type1 group
            lengthtype7 = len(type7units)
            for i in range(lengthtype7): # loop through list and take the following from Structure
                for key, val in type7units[i].items():
                    if key == 'unitCode':
                        units7.append(val)
                    if key == 'unitTitle':
                        units7.append(val)
                    if key == 'unitPoints':
                        units7.append(val)
                    if key == 'unitURL':
                        units7.append(val)
        except: type7 = "No Type 7"

        try: 
            type8 = typeNames[7]
            lengthtype8 = len(type8)
            type8units = []
            for i in range(lengthtype8): # loop through list
                for key, val in type8[i].items():
                    if key == 'typeName': # e.g., conversion, core, option, etc.
                        units8.append(val)
                    if key == 'typeInto': # if there is any typeInto field, include this
                        units8.append(val) 
                    type8units = val # creates list with dictionary of units in type1 group
            lengthtype8 = len(type8units)
            for i in range(lengthtype8): # loop through list and take the following from Structure
                for key, val in type8units[i].items():
                    if key == 'unitCode':
                        units8.append(val)
                    if key == 'unitTitle':
                        units8.append(val)
                    if key == 'unitPoints':
                        units8.append(val)
                    if key == 'unitURL':
                        units8.append(val)
        except: type8 = "No Type 8"

# NEED TO LOOK AT ADDING MORE POTENTIALLY - E.G., COURSE ID 71580 HAS 8 LEVELS (I.E., TYPES). Does any other
# degrees have more than 8 ? /C 

        return render_template('3grid-createstudyplan.html', 
            units1=units1,
            units2=units2,
            units3=units3,
            units4=units4,
            units5=units5,
            units6=units6,
            units7=units7,
            units8=units8,
            selectedCourse=selectedCourse, 
            selectedMajor=selectedMajor,
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