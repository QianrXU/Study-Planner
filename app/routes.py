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

#There might be a tidier way to do this if I can figure out how to get the column names.
#This sets up the dictionary in which study plan units can be stored.
SP_dict={}

# Set up the unit names as empty strings so that if a user has unassigned units the page will show them as
# empty boxes.
SP_dict['Y1S1_1']=""
SP_dict['Y1S1_2']=""
SP_dict['Y1S1_3']=""
SP_dict['Y1S1_4']=""
SP_dict['Y1S1_5']=""

SP_dict['Y1S2_1']=""
SP_dict['Y1S2_2']=""
SP_dict['Y1S2_3']=""
SP_dict['Y1S2_4']=""
SP_dict['Y1S2_5']=""

SP_dict['Y2S1_1']=""
SP_dict['Y2S1_2']=""
SP_dict['Y2S1_3']=""
SP_dict['Y2S1_4']=""
SP_dict['Y2S1_5']=""

SP_dict['Y2S2_1']=""
SP_dict['Y2S2_2']=""
SP_dict['Y2S2_3']=""
SP_dict['Y2S2_4']=""
SP_dict['Y2S2_5']=""
SP_dict['selectedCourse']=""
SP_dict['selectedMajor']=""
SP_dict['faculty']=""
SP_dict['coursecode']=""

# Index page
@app.route('/')
@app.route('/index', methods=['GET', 'POST'])
def index():
    return render_template('index.html', title='Home') # when the server runs, the page should show up with a title named 'Home'

# Signup function for users
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
    return render_template('signup.html', title='Sign Up', form=form) # the page should show up with a title named 'Sign Up' and display the signup form.

# Login function for users. 
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

    return render_template('login.html', title="Log In", form=form) # the page should show up with a title named 'Log in' and display the login form.


# Logout function for logged in users.
@app.route('/logout', methods=['GET', 'POST'])
@login_required # Users need to login before clicking the logout tab.
def logout():
    logout_user()
    return redirect(url_for('index')) # The web page will be redirected to the index page (home page).


# Account Page for logged in users. 
@app.route('/account', methods=['GET', 'POST'])
def account():
    #Adapted code from https://python-adv-web-apps.readthedocs.io/en/latest/flask_db2.html
    
    #Is user logged in as their user_id or their email?
    
    #Get user account
    user=current_user.id
    #check if user has saved study plans. Saves query to variable name.
    saved_study_plans=Four_Sem_SP.query.filter_by(user_id=user).order_by(Four_Sem_SP.date_updated).all()
    #initialize results and study plan array.
    results=0
    SP_array = []
    
    #if study plan found in database, then set results value to the number of rows the query returns.
    if  saved_study_plans:
        results= saved_study_plans.count()

    #If post request then the delete or load function has been called.
    if request.method == 'POST':
        #Identifies study plan user is interacting with.
        SP_id = request.form.get('SP_id')
        #Identifies if they want to load a study plan or not.
        redir = request.form.get('redir')

        #If redir is false, then delete study plan.
        if redir=='False':
            #SQLAlchemy for deleting a row.
            Four_Sem_SP.query.filter_by(study_plan_id=SP_id).delete()
            
            #Rerun the original query
            saved_study_plans #get updated study plan list
            results #get new results number
            #Reload the myaccount page.
            return render_template('account.html', title="My Account", SP_array=SP_array, results=results)
        #If redir is true, then load study plan into 3grid-createstudyplan.html'
        else:
            #Get all study plan values
            study_plan=Four_Sem_SP.query.filter_by(study_plan_id=SP_id)

            #Loop through SP_dict dictionary and use the key value to access the 
            #correlating value in the study_plan query.
            for value in SP_dict:
                data=study_plan.value
                #If statement to avoid null pointer exceptions.
                if data is not None:
                  SP_dict[value]=data 

            #Send relevant data to the
            return render_template('3grid-createstudyplan.html', 
            SP_dict=SP_dict,
            title="Create study plan"
            )

    #If not post method and when saved_study_plans returns at least 1 row.
    if results>0:
        #loop through rows from query.
        for SP in saved_study_plans:
            #Save study plan id so that it can be identified in the webpage.
            SP_key=SP.study_plan_id
            #Save data so that it can be named in the study plan list.
            SP_name= SP.date_updated
            #Add to the study plan array so it can easily be sent to the web page.
            SP_array.append( (SP_key, SP_name) )
    return render_template('account.html', title="My Account", SP_array=SP_array, results=results)

    


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
    global df

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
    # Currently only checking ListMajors, not ListMajors2 (some courses seem to add them in there for some reason)
    # Maybe there is a way to concatenate them? /C
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
            getUnitValues = df[df.Title.eq(selectedCourse)] # get dataframe for selected course, to be used in Units
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
        global selectedCourse

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
        # would be nice to remove the unitcode before the major title, if we do this we would have to
        # make changes to majorCode below though as that splits the majors text (I believe) /C

        # retrieve selected major
        if request.method == 'POST':
            try:
                selectedMajor = request.form.get('name') # saves selected major into variable
            except:
                return render_template('404.html'), 404
            return ('', 204) # indicates post response has been done successfully

        # redirect for degrees with no majors/specialisations
        lengthOfMajorsList = len(majors) # the length of the majors list will be 1 for all degrees that do not contain majors. we'll want to redirect users to the third step if there is no majors
        if lengthOfMajorsList == 1:
            return redirect(url_for('createstudyplanSelectUnits'), code=302)

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

        #replace unit selection for degree if the user has selected a major or specification - choose the values that are
        #in the structure column for this courseID instead
        majorCode = selectedMajor
        noMajor = "No major or specification available"
        if noMajor not in majorCode:
            majorCode = selectedMajor.split() # need to split as unitCode in index first and then major title
            majorCode = majorCode[0]
            getUnitValues = df[df.CourseID.eq(majorCode)] # change to selectedMajor
            coursecode = majorCode

        # process units based on course selection
        unitValues = getUnitValues['Structure'] # create dataframe of listmajors column
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
                        units1.append("&*:") #something random to split by on the frontend
                    if key == 'typeInto': # if there is any typeInto field, include this
                        units1.append(val)
                        units1.append("&*:")
                    type1units = val # creates list with dictionary of units in type1 group
            lengthtype1 = len(type1units)
            for i in range(lengthtype1): # loop through list and take the following from Structure
                for key, val in type1units[i].items():
                    if key == 'unitCode':
                        unitCode = val # save in variable to append to below for the correct output (formatting - do not want any commas between these two appends)
                    if key == 'unitTitle':
                        units1.append(unitCode + " " + val)
                    # if key == 'unitPoints':
                    #     units1.append(val)
                    # if key == 'unitURL':
                    #     units1.append(val)
        except: type1 = "No Type 1"

        try: 
            type2 = typeNames[1]
            lengthtype2 = len(type2)
            type2units = []
            for i in range(lengthtype2): # loop through list
                for key, val in type2[i].items():
                    if key == 'typeName': # e.g., conversion, core, option, etc.
                        units2.append(val)
                        units2.append("&*:") #something random to split by on the frontend
                    if key == 'typeInto': # if there is any typeInto field, include this
                        units2.append(val) 
                        units2.append("&*:") #something random to split by on the frontend
                    type2units = val # creates list with dictionary of units in type1 group
            lengthtype2 = len(type2units)
            for i in range(lengthtype2): # loop through list and take the following from Structure
                for key, val in type2units[i].items():
                    if key == 'unitCode':
                        unitCode = val # save in variable to append to below for the correct output (formatting - do not want any commas between these two appends)
                    if key == 'unitTitle':
                        units2.append(unitCode + " " + val)
                    # if key == 'unitPoints':
                    #     units2.append(val)
                    # if key == 'unitURL':
                    #     units2.append(val)
        except: type2 = "No Type 2"

        try: 
            type3 = typeNames[2]
            lengthtype3 = len(type3)
            type3units = []
            for i in range(lengthtype3): # loop through list
                for key, val in type3[i].items():
                    if key == 'typeName': # e.g., conversion, core, option, etc.
                        units3.append(val)
                        units3.append("&*:") #something random to split by on the frontend
                    if key == 'typeInto': # if there is any typeInto field, include this
                        units3.append(val) 
                        units3.append("&*:") #something random to split by on the frontend
                    type3units = val # creates list with dictionary of units in type1 group
            lengthtype3 = len(type3units)
            for i in range(lengthtype3): # loop through list and take the following from Structure
                for key, val in type3units[i].items():
                    if key == 'unitCode':
                        unitCode = val # save in variable to append to below for the correct output (formatting - do not want any commas between these two appends)
                    if key == 'unitTitle':
                        units3.append(unitCode + " " + val)
                    # if key == 'unitPoints':
                    #     units3.append(val)
                    # if key == 'unitURL':
                    #     units3.append(val)
        except: type3 = "No Type 3"

        try: 
            type4 = typeNames[3]
            lengthtype4 = len(type4)
            type4units = []
            for i in range(lengthtype4): # loop through list
                for key, val in type4[i].items():
                    if key == 'typeName': # e.g., conversion, core, option, etc.
                        units4.append(val)
                        units4.append("&*:") #something random to split by on the frontend
                    if key == 'typeInto': # if there is any typeInto field, include this
                        units4.append(val) 
                        units4.append("&*:") #something random to split by on the frontend
                    type4units = val # creates list with dictionary of units in type1 group
            lengthtype4 = len(type4units)
            for i in range(lengthtype4): # loop through list and take the following from Structure
                for key, val in type4units[i].items():
                    if key == 'unitCode':
                        unitCode = val # save in variable to append to below for the correct output (formatting - do not want any commas between these two appends)
                    if key == 'unitTitle':
                        units4.append(unitCode + " " + val)
                    # if key == 'unitPoints':
                    #     units4.append(val)
                    # if key == 'unitURL':
                    #     units4.append(val)
        except: type4 = "No Type 4"
        
        try: 
            type5 = typeNames[4]
            lengthtype5 = len(type5)
            type5units = []
            for i in range(lengthtype5): # loop through list
                for key, val in type5[i].items():
                    if key == 'typeName': # e.g., conversion, core, option, etc.
                        units5.append(val)
                        units5.append("&*:") #something random to split by on the frontend
                    if key == 'typeInto': # if there is any typeInto field, include this
                        units5.append(val) 
                        units5.append("&*:") #something random to split by on the frontend
                    type5units = val # creates list with dictionary of units in type1 group
            lengthtype5 = len(type5units)
            for i in range(lengthtype5): # loop through list and take the following from Structure
                for key, val in type5units[i].items():
                    if key == 'unitCode':
                        unitCode = val # save in variable to append to below for the correct output (formatting - do not want any commas between these two appends)
                    if key == 'unitTitle':
                        units5.append(unitCode + " " + val)
                    # if key == 'unitPoints':
                    #     units5.append(val)
                    # if key == 'unitURL':
                    #     units5.append(val)
        except: type5 = "No Type 5"
        
        try: 
            type6 = typeNames[5]
            lengthtype6 = len(type6)
            type6units = []
            for i in range(lengthtype6): # loop through list
                for key, val in type6[i].items():
                    if key == 'typeName': # e.g., conversion, core, option, etc.
                        units6.append(val)
                        units6.append("&*:") #something random to split by on the frontend
                    if key == 'typeInto': # if there is any typeInto field, include this
                        units6.append(val) 
                        units6.append("&*:") #something random to split by on the frontend
                    type6units = val # creates list with dictionary of units in type1 group
            lengthtype6 = len(type6units)
            for i in range(lengthtype6): # loop through list and take the following from Structure
                for key, val in type6units[i].items():
                    if key == 'unitCode':
                        unitCode = val # save in variable to append to below for the correct output (formatting - do not want any commas between these two appends)
                    if key == 'unitTitle':
                        units6.append(unitCode + " " + val)
                    # if key == 'unitPoints':
                    #     units6.append(val)
                    # if key == 'unitURL':
                    #     units6.append(val)
        except: type6 = "No Type 6"

        try: 
            type7 = typeNames[6]
            lengthtype7 = len(type7)
            type7units = []
            for i in range(lengthtype7): # loop through list
                for key, val in type7[i].items():
                    if key == 'typeName': # e.g., conversion, core, option, etc.
                        units7.append(val)
                        units7.append("&*:") #something random to split by on the frontend
                    if key == 'typeInto': # if there is any typeInto field, include this
                        units7.append(val) 
                        units7.append("&*:") #something random to split by on the frontend
                    type7units = val # creates list with dictionary of units in type1 group
            lengthtype7 = len(type7units)
            for i in range(lengthtype7): # loop through list and take the following from Structure
                for key, val in type7units[i].items():
                    if key == 'unitCode':
                        unitCode = val # save in variable to append to below for the correct output (formatting - do not want any commas between these two appends)
                    if key == 'unitTitle':
                        units7.append(unitCode + " " + val)
                    # if key == 'unitPoints':
                    #     units7.append(val)
                    # if key == 'unitURL':
                    #     units7.append(val)
        except: type7 = "No Type 7"

        try: 
            type8 = typeNames[7]
            lengthtype8 = len(type8)
            type8units = []
            for i in range(lengthtype8): # loop through list
                for key, val in type8[i].items():
                    if key == 'typeName': # e.g., conversion, core, option, etc.
                        units8.append(val)
                        units8.append("&*:") #something random to split by on the frontend
                    if key == 'typeInto': # if there is any typeInto field, include this
                        units8.append(val) 
                        units8.append("&*:") #something random to split by on the frontend
                    type8units = val # creates list with dictionary of units in type1 group
            lengthtype8 = len(type8units)
            for i in range(lengthtype8): # loop through list and take the following from Structure
                for key, val in type8units[i].items():
                    if key == 'unitCode':
                        unitCode = val # save in variable to append to below for the correct output (formatting - do not want any commas between these two appends)
                    if key == 'unitTitle':
                        units8.append(unitCode + " " + val)
                    # if key == 'unitPoints':
                    #     units8.append(val)
                    # if key == 'unitURL':
                    #     units8.append(val)
        except: type8 = "No Type 8"

# NEED TO LOOK AT ADDING MORE POTENTIALLY - E.G., COURSE ID 71580 HAS 8 LEVELS (I.E., TYPES). Does any other
# degrees have more than 8 ? Look at 31400 I think it went over.
# # Doctor of Podiatry, completely different again. Need to rethink /C 

        return render_template('3grid-createstudyplan.html', 
            units1=units1,
            units2=units2,
            units3=units3,
            units4=units4,
            units5=units5,
            units6=units6,
            units7=units7,
            units8=units8,
            majorCode=majorCode,
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
    return render_template('faq.html', title="FAQ") # the page should show up with a title named 'FAQ'

# 404 Page
@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

if __name__ == '__main__':
    app.run(debug=True)