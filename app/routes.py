from signal import valid_signals
from tkinter import Y
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
    
    #declare global variables (must be same as global variables for createstudyplanSelectUnits())
    global selectedCourse 
    global selectedMajor
    global faculty
    global coursecode
    global getUnitValues
    global SP_dict

    #Get user account
    user=current_user.id
    #check if user has saved study plans. Saves query to variable name.
    saved_study_plans=Four_Sem_SP.query.filter_by(user_id=user).order_by(Four_Sem_SP.date_updated).all()
    #initialize number of results gotten from query and study plan array. 
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

        #If redir is true, then load study plan information
        else:
            #Get study plan values
            study_plan=Four_Sem_SP.query.filter_by(study_plan_id=SP_id).one()
            
            SP_dict['Y1S1_1']=study_plan.Y1S1_1
            SP_dict['Y1S1_2']=study_plan.Y1S1_2
            SP_dict['Y1S1_3']=study_plan.Y1S1_3
            SP_dict['Y1S1_4']=study_plan.Y1S1_4
            SP_dict['Y1S1_5']=study_plan.Y1S1_5

            SP_dict['Y1S2_1']=study_plan.Y1S2_1
            SP_dict['Y1S2_2']=study_plan.Y1S2_2
            SP_dict['Y1S2_3']=study_plan.Y1S2_3
            SP_dict['Y1S2_4']=study_plan.Y1S2_4
            SP_dict['Y1S2_5']=study_plan.Y1S2_5

            SP_dict['Y2S1_1']=study_plan.Y2S1_1
            SP_dict['Y2S1_2']=study_plan.Y2S1_2
            SP_dict['Y2S1_3']=study_plan.Y2S1_3
            SP_dict['Y2S1_4']=study_plan.Y2S1_4
            SP_dict['Y2S1_5']=study_plan.Y2S1_5

            SP_dict['Y2S2_1']=study_plan.Y2S2_1
            SP_dict['Y2S2_2']=study_plan.Y2S2_2
            SP_dict['Y2S2_3']=study_plan.Y2S2_3
            SP_dict['Y2S2_4']=study_plan.Y2S2_4
            SP_dict['Y2S2_5']=study_plan.Y2S2_5 

            #Assign values from study plan to global variables.
            selectedCourse=study_plan.selectedCourse
            selectedMajor=study_plan.selectedMajor
            faculty=study_plan.faculty
            coursecode=study_plan.coursecode

            if len(selectedMajor)<1:
                selectedMajor="No major or specialisation available"
            
            #create df
            targetcsv = os.path.join(app.static_folder, 'Json-export.csv')
            df = pd.read_csv(targetcsv, sep=",")
            # Process data
            selectedYear = 2022 # Filters courses by year determined on the left. Change value to other year if wanted/needed.
            df = df[df.Year.eq(selectedYear)]
            df = df[df.Availability.str.contains("current / "+str(selectedYear))] # Filter courses that are available in the given year (year provided in selectedYear variable)
            df = df[df['Structure'].notna()] # Removes all options from dataframe where Structure cell is empty

            getUnitValues = df[df.Title.eq(selectedCourse)] # get dataframe for selected course, to be used in Units

            #create df
            targetcsv = os.path.join(app.static_folder, 'Json-export.csv')
            df = pd.read_csv(targetcsv, sep=",")
            # Process data
            selectedYear = 2022 # Filters courses by year determined on the left. Change value to other year if wanted/needed.
            df = df[df.Year.eq(selectedYear)]
            df = df[df.Availability.str.contains("current / "+str(selectedYear))] # Filter courses that are available in the given year (year provided in selectedYear variable)
            df = df[df['Structure'].notna()] # Removes all options from dataframe where Structure cell is empty

            getUnitValues = df[df.Title.eq(selectedCourse)] # get dataframe for selected course, to be used in Units

            getMasterDegrees(df, selectedCourse) # assigns spec and core values

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
    global coursecode
    global SP_dict
    global selectedStart

    #Clear any saved study plan data
    for item in SP_dict.keys():
        SP_dict[item]=''

    # Save csv file into dataframe
    targetcsv = os.path.join(app.static_folder, 'Json-export.csv')
    df = pd.read_csv(targetcsv, sep=",")

    # Process data
    selectedYear = 2022 # Filters courses by year determined on the left. Change value to other year if wanted/needed.
    #df = df[df.Year.eq(selectedYear)]
    df = df[df.Availability.str.contains("current / "+str(selectedYear))] # Filter courses that are available in the given year (year provided in selectedYear variable)
    df = df[df['Structure'].notna()] # Removes all options from dataframe where Structure cell is empty

    # filter out combined bachelors/masters and doctorates
    #df = df[df.Title.str.contains("Master")] # Filter out all master's degrees
    #df = df[~df.Title.str.contains("Bachelor|Doctor")] # Filter out all combined masters/bachelors and dmasters/octorates from df (~ means inverse)

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
            selectedStart = request.form.get('selectedStart') # saves selected course into variable
            
            getMasterDegrees(df, selectedCourse) # send selected course and dataframe to function
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
            faculty=faculty,
            degrees_withID=degrees_withID,
            degrees=degrees, 
            title="Create study plan")


def getMasterDegrees(data, selectedCourse):
    global m_specialisations_list
    global m_levelNames_list
    global m_specialisations
    global m_levelNamesCore
    global core
    global spec

    # get fields we're interested in
    masterCourses = data[["Year", "CourseID", "Title", "ListMajors2", "Faculty", "Structure", "Availability", "IntakePeriods", "StandardFullTimeCompletion"]] # only interested in these variables
    masterCourse = masterCourses[masterCourses.Title.eq(selectedCourse)] # really only interested in the course the user has selected
    structure = masterCourse['Structure']

    # Below starts the processing of the structure column.
    # this holds important information about specialisations, 
    # unit groups and units
    structureProcessing = [str(x) for x in structure][0]
    structureProcessing = structureProcessing[1:-1]
    structureProcessing = json.loads(structureProcessing) # convert into json/list

    # 'introduction', 'levelsspecials'; bottom layer of structure
    m_items = structureProcessing.items() # keys on this dict will provide bottom layer of information: ['introduction', 'levelsSpecials']
    m_info = [] #'introduction'
    m_levelsSpecials = [] #'levelsSpecials'
    for k, v in m_items: #
        if k == "introduction": 
            m_info.append(v) # if selected unit group has an introduction, save it to m_info variable
        if k == "levelsSpecials":
            m_levelsSpecials.append(v)

    # levelnames, i.e., unit groups
    m_levelNames = [] # levelnames = unit group names - ALL, with unit data after append
    m_levelNames_list = []
    m_levelNamesCore = [] # levelnames = unit group names - ONLY core/conversion, with unit data after append
    m_specialisations = [] # levelnames = unit group names - ONLY specialisations, with unit data after append
    m_specialisations_list = [] # levelnames = unit group names - ONLY specialisation names
    [unitgroup] = m_levelsSpecials # delist m_levelsSpecials (i.e., reduce by one list level), otherwhise the list length (used in range below) will not be correct. 

    for i in range(len(unitgroup)): # count the amount of unitgroups that exist and process each one
        for k, v in unitgroup[i].items(): # keys are: ['levelName', 'typeInto', 'unitTypes']
            if k == "levelName":
                #m_levelNames
                m_levelNames.append(v) # v = 'conversion', 'core' etc., but also all specialisations, e.g., 'biomedical engineering specialisation'
                m_levelNames_list.append(v)
                # m_specialisations
                substring = "specialisation"
                if substring in v:
                    m_specialisations_list.append(v) # to be used in major/specialisation selection
                    m_specialisations.append(v) # append all specialisations in levelNames to m_specialisations
                    for k, v in unitgroup[i].items():
                         if k == "unitTypes":
                            m_specialisations.append(v)

                #m_levelNamesCore
                else:
                    m_levelNamesCore.append(v) # append all other levelNames to m_levelNamesCore
                    for k, v in unitgroup[i].items():
                         if k == "unitTypes":
                            m_levelNamesCore.append(v)

    # this dict will hold the core/conversion units for a degree with a major/specialisation
    core = {}
    for i in range(0, len(m_levelNamesCore), 2):
        x = str([m_levelNamesCore[i]])
        y = str([m_levelNamesCore[i+1]])
        core[x] = y

    # this dict will hold the units for all unit groups under a major/specialisation
    spec = {}
    for i in range(0, len(m_specialisations), 2):
        x = str([m_specialisations[i]])
        y = str([m_specialisations[i+1]])
        spec[x] = y

    return m_specialisations_list, m_levelNames_list, m_specialisations, m_levelNamesCore, core, spec

# STUDY PLANNER - SELECT MAJOR
@app.route('/createstudyplan-majors', methods=['GET', 'POST'])
def createstudyplanSelectMajor():
    try:
        global selectedMajor
        global getMajorValues
        global selectedCourse

        # process ListMajors column (i.e., potential majors) and potential specialisations if master is selected where specialisation is an option
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
        for specialisation in range(len(m_specialisations_list)): # m_specialisations_list contains all specialisations for the selected course (if master with specialisation)
            majors.append(m_specialisations_list[specialisation])
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
        global SP_dict

        #replace unit selection for degree if the user has selected a major or specification - choose the values that are
        #in the structure column for this courseID instead
        majorCode = selectedMajor

        noMajor = "No major or specialisation available"

        # if specialisation, change majorCode (what is displayed on frontend) to nocode (as it will show under Major: anyway!)
        if len(spec) != 0:
            majorCode = noMajor

        if noMajor not in majorCode:
            majorCode = selectedMajor.split() # need to split as unitCode in index first and then major title
            majorCode = majorCode[0]
            coursecode = majorCode
            getUnitValues = df[df.CourseID.eq(majorCode)] # change to selectedMajor
            #coursecode = majorCode
        
        if len(spec) == 0:
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

        if len(spec) > 0: # if there are specialisations
            typeNames = []
            for y in range(1, len(m_levelNamesCore), 2): # start from index 1 and increment by 2. m_levelNamesCore needs to be appended too as they are core regardless of specialisation
                typeNames.append(m_levelNamesCore[y]) # the appended typenames from this variable will be core and conversion units that are mutual for all specialisations regardless of which one

            for i in range(len(m_specialisations)):
                if selectedMajor == m_specialisations[i]: # if the selected major is in the m_specialisations variable ...
                    index = m_specialisations.index(selectedMajor) # ... find the index of that variable and pop and ...
                    typeNames.append(m_specialisations[index+1]) # ... append the specialisation data to typenames

        units = [] # all unit codes + unit titles to be saved into this list 
        unitCodeList = [] # all unit codes to be saved into this list (for connecting with unit list.csv on frontend)

        credits = {}

        try: 
            length = len(typeNames)
            for y in range(length):
                types = typeNames[y]
                lengthoftypes = length = len(types)

                for i in range(lengthoftypes): # loop through list

                    #if lengthoftypes == 1 or lengthoftypes > 1:
                    for key, val in types[i].items():
                        if key == 'typeName': # e.g., conversion, core, option, etc.
                            units.append(val)
                            units.append("***") #something random to split by on the frontend
                        if key == 'typeInto': # if there is any typeInto field, include this
                            units.append(val)
                            units.append("***")
                        typesOfunits = val # creates list with dictionary of units

                    lengthtype1 = len(typesOfunits)
                    for i in range(lengthtype1): # loop through list and take the following from Structure
                        for key, val in typesOfunits[i].items():
                            if key == 'unitCode':
                                unitCode = val # save in variable to append to below for the correct output (formatting - do not want any commas between these two appends)
                                unitCodeList.append(val)
                            if key == 'unitTitle':
                                unitTitle = val
                                units.append(unitCode + " " + val + "***")
                            if key == 'unitPoints':
                                credits[unitCode + " " + unitTitle] = val
                    units.append("NEXT_UNIT_ROLE") #something random to split by on the frontend
                    
        except:
            units.append("No units")

        #import and read unit list into unitscsv variable
        unitInfoCsv = os.path.join(app.static_folder, 'Unit list.csv')
        unitInfoCsv = pd.read_csv(unitInfoCsv, sep=",")
        unitInfoCsv = unitInfoCsv[unitInfoCsv.Code.isin(unitCodeList)] # filter 'Unit list.csv' by units in selected degree/major/specialisation
        availability = dict(zip(unitInfoCsv.Code + " " + unitInfoCsv.Title + "***", unitInfoCsv.Availabilities + "***"))
        
        # variables for unit information modal (click on modal)
        prereq = dict(zip(unitInfoCsv.Code + " " + unitInfoCsv.Title, unitInfoCsv.Prerequisites))
        prereq = json.dumps(prereq)
        corereq = dict(zip(unitInfoCsv.Code + " " + unitInfoCsv.Title, unitInfoCsv.Corequisites))
        corereq = json.dumps(corereq)
        incomp = dict(zip(unitInfoCsv.Code + " " + unitInfoCsv.Title, unitInfoCsv.Incompatibilities))
        incomp = json.dumps(incomp)
        outcomes = dict(zip(unitInfoCsv.Code + " " + unitInfoCsv.Title, unitInfoCsv.Outcomes))
        outcomes = json.dumps(outcomes)
        content = dict(zip(unitInfoCsv.Code + " " + unitInfoCsv.Title, unitInfoCsv.Content))
        content = json.dumps(content)
        credits = json.dumps(credits)

        #Add Code and Prerequisites from unit list.csv to dictinary
        prerequists = dict(zip(unitInfoCsv.Code, unitInfoCsv.Prerequisites))
        prerequists=json.dumps(prerequists)
        return render_template('3grid-createstudyplan.html', 
            selectedStart=selectedStart,
            getUnitValues=getUnitValues,
            unitCodeList=unitCodeList,
            availability=availability,
            units=units,
            majorCode=majorCode,
            selectedCourse=selectedCourse, 
            selectedMajor=selectedMajor,
            faculty=faculty,
            coursecode=coursecode,
            prerequists = prerequists,
            prereq=prereq,
            corereq=corereq,
            incomp=incomp,
            outcomes=outcomes,
            content=content,
            credits=credits,
            SP_dict=SP_dict,
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