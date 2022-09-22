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
    return render_template('signup.html', title='Sign up', form=form) # the page should show up with a title named 'Sign Up' and display the signup form.

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
        next_page = request.args.get('account')
        if not next_page or url_parse(next_page).netloc != '':
            return redirect(url_for('account'))
        return redirect('account')

    return render_template('login.html', title="Log in", form=form) # the page should show up with a title named 'Log in' and display the login form.


# Logout function for logged in users.
@app.route('/logout', methods=['GET', 'POST'])
@login_required # Users need to login before clicking the logout tab.
def logout():
    logout_user()
    return redirect(url_for('index')) # The web page will be redirected to the index page (home page).


# Account Page for logged in users.  
### Python for account page written by Georgia Jefferson ###
@app.route('/account', methods=['GET', 'POST'])
def account():
    #Adapted code from https://python-adv-web-apps.readthedocs.io/en/latest/flask_db2.html
    
    #declare global variable
    global SP_dict

    #Get user account
    user=current_user.id
    #check if user has saved study plans. Saves query to variable name.
    saved_study_plans=Four_Sem_SP.query.filter_by(user_id=user).order_by(Four_Sem_SP.date_updated).all()
    #initialize results and study plan array.
    results=0
    SP_array = []
    
    #if study plan found in database, then set results value to the number of rows the query returns.
    if  saved_study_plans:
        results= len(saved_study_plans)

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
            db.session.commit()

            return ('', 204) # indicates post response has been done successfully


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

            return ('', 204) # indicates post response has been done successfully

    #If not post method and when saved_study_plans returns at least 1 row.
    if results>0:
        #loop through rows from query.
        for SP in saved_study_plans:
            #Save study plan id so that it can be identified in the webpage.
            SP_key=SP.study_plan_id
            #Save data so that it can be named in the study plan list.
            SP_name= SP.date_updated.strftime( "%d/%m/%Y" )
            #Add to the study plan array so it can easily be sent to the web page.
            SP_array.append( (SP_key, SP_name) )
    return render_template('account.html', title="My Account", SP_array=SP_array, results=results)

    


# STUDY PLANNER - SELECT COURSE
# in this function we focus on processing the json-export.csv file so that users can select the degree they are interested in
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
    global SP_dict
    global coursecode

    # Save csv file into dataframe
    targetcsv = os.path.join(app.static_folder, 'Json-export.csv')
    df = pd.read_csv(targetcsv, sep=",")

    # Process data
    selectedYear = 2022 # Filters courses by year determined on the left. Change value to other year if wanted/needed.
    df = df[df.Year.eq(selectedYear)]
    df = df[df.Availability.str.contains("current / "+str(selectedYear))] # Filter courses that are available in the given year (year provided in selectedYear variable)
    df = df[df['Structure'].notna()] # Removes all options from dataframe where Structure cell is empty

    # Degrees variable processing - this is the dataframe that the Course selection dropdown will get its values from.
    degrees = df[~df.CourseID.str.contains('MJD|MJS')] # remove any course IDs that start with MJD or MJS (majors or second majors).
    degrees = dict(zip(degrees.Title, degrees.CourseID))
    degrees = sorted(degrees.keys())

    degrees_withID = dict(zip(df.Title, df.CourseID))
    degrees_withFaculty = dict(zip(df.Title, df.Faculty))
    faculty = dict(zip(df.Faculty, df.CourseID))

    # TO DO - Need to check if selected degree ListMajors and ListMajors2 empty, 
    # Currently only checking ListMajors, not ListMajors2 (some courses seem to add them in there for some reason)
    # Maybe there is a way to concatenate them? /C
    selectedMajor = "No major or specialisation available"

    if request.method == 'POST':
        try:
            selectedCourse = request.form.get('name') # saves selected course into variable
            getMasterDegrees(df, selectedCourse) # send selected course and dataframe to function
            SP_dict['selectedCourse'] = selectedCourse
            for key, value in degrees_withID.items(): # iterates through values to find course code
                if selectedCourse == key:
                    coursecode=value
                    SP_dict['coursecode'] = value
            for key, value in degrees_withFaculty.items(): # iterates through values to find course code
                if selectedCourse == key:
                    faculty=value
                    SP_dict['faculty'] = value
            getMajorValues = df[df.Title.eq(selectedCourse)] # get dataframe for selected course, to be used in Major 
            getUnitValues = df[df.Title.eq(selectedCourse)] # get dataframe for selected course, to be used in Units
        except:
            return render_template('404.html'), 404
        return ('', 204) # indicates post response has been done successfully

    return render_template('1course-createstudyplan.html',
            #faculty=SP_dict['faculty'],

            faculty=faculty,
            degrees_withID=degrees_withID,
            degrees=degrees, 
            title="Create study plan")

def getMasterDegrees(data, selectedCourse):
    global masterCourses
    global masterprocess # don't forget to remove redundant global vars !!

    # get fields we're interested in
    masterCourses = data[["Year", "CourseID", "Title", "ListMajors2", "Faculty", "Structure", "Availability", "IntakePeriods", "StandardFullTimeCompletion"]] # only interested in these variables
    masterCourse = masterCourses[masterCourses.Title.eq(selectedCourse)] # really only interested in the course the user has selected
    structure = masterCourse['Structure']

    # Below starts the processing of the structure column.
    # this holds important information about specialisations, 
    # unit groups and units
    
    #pd.set_option("display.max_colwidth", 99999) # need to set to a very high value otherwise this pandas method truncates the string velow
    #structureProcessing = structure.to_string(index = False) # unpack outer list layer so its valid json for getting thrown into the json loads method below
    structureProcessing = [str(x) for x in structure][0]
    structureProcessing = structureProcessing[1:-1]
    structureProcessing = json.loads(structureProcessing) # convert into json/list

    masterprocess = structureProcessing
    print(structureProcessing)

    # 'introduction', 'levelsspecials'; bottom layer of structure
    m_items = structureProcessing.items() # keys on this dict will provide bottom layer of information: ['introduction', 'levelsSpecials']
    m_info = [] #'introduction'
    m_levelsSpecials = [] #'levelsSpecials'
    for k, v in m_items:
        if k == "introduction": 
            m_info.append(v) # if selected unit group has an introduction, save it to m_info variable
        if k == "levelsSpecials":
            m_levelsSpecials.append(v)
            #print(m_levelsSpecials)

    print("###################")


    # levelnames, i.e., unit groups
    m_levelNames = [] # levelnames = unit group names
    m_typeName = []
    [unitgroup] = m_levelsSpecials # delist m_levelsSpecials (i.e., reduce by one list level). 
    for i in range(len(unitgroup)): # count the amount of unitgroups that exist and pull out each one
        for k, v in unitgroup[i].items(): # keys are: ['levelName', 'typeInto', 'unitTypes']
            if k == "levelName":
                m_levelNames.append(v) 
                #print(v)
        
            # process units under each unit group
            if k == "unitTypes":
                m_typeName.append(v)

    # typeNames
    units = []
    for i in range(len(m_typeName)): # print the number of typeNames present. 
        [delist] = m_typeName[i] # delist each item (unit group) in m_types to convert it to a dictionary
        for k, v in delist.items(): # keys are: ['typeName', 'typeInto', 'units']
            if k == "typeName":
                units.append(v)
            if k == "typeInto":
                units.append(v)

            # one step deeper
            if k == "units":
                units.append(v)
            
    print(units)


    print("######  COMPLETE #######")



    #print(m_levelNames)
    

    return masterCourses, masterprocess



""" 

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
            
"""





# STUDY PLANNER - SELECT MAJOR
@app.route('/createstudyplan-majors', methods=['GET', 'POST'])
def createstudyplanSelectMajor():
    try:
        global selectedMajor
        global getMajorValues
        global selectedCourse
        global SP_dict

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
                SP_dict['selectedMajor'] = request.form.get('name') # saves selected major into variable
            except:
                return render_template('404.html'), 404
            return ('', 204) # indicates post response has been done successfully

        # redirect for degrees with no majors/specialisations
        lengthOfMajorsList = len(majors) # the length of the majors list will be 1 for all degrees that do not contain majors. we'll want to redirect users to the third step if there is no majors
        # if lengthOfMajorsList == 1:
        #     return redirect(url_for('createstudyplanSelectUnits'), code=302)

        return render_template('2major-createstudyplan.html',
            masterprocess=masterprocess,
            masterCourses=masterCourses,
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
        global SP_dict

        #replace unit selection for degree if the user has selected a major or specification - choose the values that are
        #in the structure column for this courseID instead
        majorCode = selectedMajor
        noMajor = "No major or specialisation available"
        if noMajor not in majorCode:
            majorCode = selectedMajor.split() # need to split as unitCode in index first and then major title
            majorCode = majorCode[0]
            coursecode = majorCode
            SP_dict['courseCode'] = majorCode
            getUnitValues = df[df.CourseID.eq(majorCode)] # change to selectedMajor
            #coursecode = majorCode

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

        units = [] # all unit codes + unit titles to be saved into this list 
        unitCodeList = [] # all unit codes to be saved into this list (for connecting with unit list.csv on frontend)

        try: 
            length = len(typeNames)
            for y in range(length):
                types = typeNames[y]
                lengthoftypes = length = len(types)
                for i in range(lengthoftypes): # loop through list
                    for key, val in types[i].items():
                        if key == 'typeName': # e.g., conversion, core, option, etc.
                            units.append(val)
                            units.append("***") #something random to split by on the frontend
                        if key == 'typeInto': # if there is any typeInto field, include this
                            units.append(val)
                            units.append("***")
                        typesOfunits = val # creates list with dictionary of units in type1 group
                lengthtype1 = len(typesOfunits)
                for i in range(lengthtype1): # loop through list and take the following from Structure
                    for key, val in typesOfunits[i].items():
                        if key == 'unitCode':
                            unitCode = val # save in variable to append to below for the correct output (formatting - do not want any commas between these two appends)
                            unitCodeList.append(val)
                        if key == 'unitTitle':
                            units.append(unitCode + " " + val + "***")
                #units.append("&*:") #something random to split by on the frontend
                units.append("NEXT_UNIT_ROLE") #something random to split by on the frontend
                        # if key == 'unitPoints':
                        #     units1.append(val)
                        # if key == 'unitURL':
                        #     units1.append(val)
        except:
            units.append("No units")

        #import and read unit list into unitscsv variable
        unitInfoCsv = os.path.join(app.static_folder, 'Unit list.csv')
        unitInfoCsv = pd.read_csv(unitInfoCsv, sep=",")
        unitInfoCsv = unitInfoCsv[unitInfoCsv.Code.isin(unitCodeList)] # filter 'Unit list.csv' by units in selected degree/major/specialisation
        availability = dict(zip(unitInfoCsv.Code + " " + unitInfoCsv.Title + "***", unitInfoCsv.Availabilities + "***"))
        #Add Code and Prerequisites from unit list.csv to dictinary
        prerequists = dict(zip(unitInfoCsv.Code, unitInfoCsv.Prerequisites))
        prerequists=json.dumps(prerequists)
        return render_template('3grid-createstudyplan.html', 
            getUnitValues=getUnitValues,
            unitCodeList=unitCodeList,
            availability=availability,
            units=units,
            majorCode=majorCode,
            selectedCourse=selectedCourse, 
            selectedMajor=selectedMajor,
            faculty=faculty,
            #coursecode= SP_dict['courseCode'],
            coursecode=coursecode,
            prerequists = prerequists,
            title="Create study plan")
    except:
        return render_template('404.html'), 404


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