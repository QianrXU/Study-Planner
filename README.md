# Study Planner
This is the main repository and project planning page of Study Planner Team 1 (CITS5206 Professional Computing).

___

## User manual
1. Project details
2. How to run the Study Planner project
3. Database schema
4. Data
5. Functionality
   1. Sign up
   2. Log in
   3. Select units
   4. Save study plan
   5. Download study plan 
6. Testing documentation
7. Extended functionality

___

## Project details
UWA have identified a need for a tool that allows current students, prospective students, and UWA staff, to create study plans of the university’s courses. Currently, study plans are created by hand based on the unit sequence, course rules, and semester availability, which are stored in UWAs CAIDi curriculum management system. A Study Planner tool could reduce the risk of human error and thus allow for the generation of more reliable study plans.

The Study Planner project uses Flask as the backend framework and FlaskSQLAlchemy for the database. For a full list of imported libraries, please view the requirements.txt file.

___

## How to run the project
First you will want to cd to the project directory in which you want to host the Study Planner project and then clone the project files from GitHub: `git clone https://github.com/QianrXU/Study-Planner.git`

Depending on if you use Unix or Windows, follow the steps below.

### Unix
**If virtual environment not installed:** Use pip or another package manager to install the virtual environment package: `$ sudo apt-get install python3-venv`

1. cd into project folder: `$ cd Study-Planner`
2. Create a virtual environment: `$ python3 -m venv venv`
3. Activate the python virtual environment: `$ source venv/bin/activate`
4. Install prerequisites (requires python3, flask, venv, etc.): `$ pip3 install -r requirements.txt`.
5. To run the app: `$ flask run`. This should start the app running on localhost at port 5000, i.e. http://localhost:5000/index
6. To deactivate the project on localhost: `$ ^C`
7. To deactivate the virtual environment: `$ deactivate`

### Windows
**If virtual environment not installed:** Use pip or another package manager to install the virtual environment package: `> pip install virtualenv`

1. cd into project folder: `$ cd Study-Planner`
2. Create a virtual environment: `> virtualenv`
3. Activate the python virtual environment: `> .\venv\Scripts\activate`. This should start the app running on localhost at port 5000, i.e. http://localhost:5000/index.
4. Install prerequisites (requires python3, flask, venv, etc.): `> pip install -r requirements.txt`.
5. To deactivate the virtual environment: `> deactivate`
___

## Database schema

___

## Data
All course and unit data used in the Study Planner project has been exported from the UWA CAIDi system and provided to the team by UWA's Curriculum Office. Two files have been key in generating the functionality of the Study Planner tool (both to be found in the *static* subfolder), 1. Json-export.csv, and 2. Unit list.csv. Both these files are processed in *routes.py*, but also in the relevant .html pages using JavaScript (*1course-createstudyplan.html*, *2major-createstudyplan.html* and *3grid-createstudyplan.html*).

### Json-export.csv
The *Json-export.csv* file contains information on all courses at UWA between the years of 2018 and 2022.

Attributes used up to the end of Sprint 2 includes:
* CourseID
* Year
* Structure (this attribute contains all units that belong to the selected course or major/specialisation)
* ListMajors
* Title
* Faculty
* Availability (describes the availability of the course - e.g., may not be available in 2022)

Attributes we wish to incorporate in Sprint 3 includes:
* IntakePeriods - this attribute describes whether a course is available at the beginning of a year, mid-year, or both (to filter the 'select starting year/semester' dropdown)
* StandardFullTimeCompletion - this attribute desribes the standard in years of how long a course is to take to a student to be completed (will determine which grid/database is used on the 'select units' page)

### Unit list.csv
The *Unit list.csv* file is an amalgamation of three active unit sequence csv files for three Master degrees (12520 Master of Translation Studies, 62510 Master of Information Technology and 62550 Master of Professional Engineering). These three files were processed by *join_individual_unit_lists.py* - a program which concatenates and groups units by unit code and exports the result to a new .csv file, *Unit list.csv*. All four files are found in the subfolder *static* > *unit data files*.

Attributes used up to the end of Sprint 2 includes:
* Code
* Title
* Availabilities (describes the availability of the unit, e.g., Semester 1 only)

Attributes we wish to incorporate in Sprint 3 includes:
* Status (whether the unit is available in 2022 or not)
* Content (short description of the unit)
* Outcomes (short description of the outcomes of the unit)
* Corequisites (describes if there are any co-requisites to the unit)
* Incompatibilities (describes if there are any incompatible units related to the selected unit)
* Prerequisites (describes if there are any prerequisites to taking the selected unit)

### Making updates to or exchanging the .csv files
Any changes that are made to the .csv files must follow a certain ruleset. If exchanging any of the .csv files, it is important they are exported from CAIDi the same way as they were when we were initially handed the data.

**Changing the year that courses are filtered by**

In the *routes.py* file, there is a line that reads: `selectedYear = 2022`. Changing the year and saving the file will filter the data in *Json-export.csv*, i.e., course data, to only hold data for the selected year.

**Other reflections**

* The *join_individual_unit_lists.py* file is redundant should the Curriculum Office be able to produce an active sequence unit .csv file that contains all units at UWA.

___

## Functionality
### Sign up
> signup.html

This is the signup page((**Figure 1**)) for new users to register an account to create the study plan. User can enter email address and password, The password should not be less than 6 characters long. Enter the same password you have entered for password in confirm password field. Only registered user will have the access to Myaccount page that will allow user to see his/her saved study plans. Registered user can save the plans for later reference and can be deleted if not needed

|![Sign up](./readmeImages/register.PNG)|
|:--:|
| <b> Figure 1</b>|

### Login
> login.html

If the user is registered, the user can login using his/her credentials that used at the time of registration. User can use this login page(**Figure 2**) to create, save and delete study plans. If the user enters wrong credentials, the system will alert this and ask to enter correct details. This page also has 'remember me' functionality that allows user to save his/her login information and do not have to be enter the details each login time. If the user is not registered, he can click 'Don't have an account?' link to directs to sign up page. We will be adding forgot password actionality in sprint 3.

|![Login](./readmeImages/login.PNG)|
|:--:|
| <b> Figure 2</b>|

### Home Page
> index.html

All users(registered or not registered) are able to access this page (**Figure 3**) and create study plan, but only the registered users will be able to save the study plan. Clicking 'Create study Plan' directs the user to the course selection page.

|![Home Page](./readmeImages/home.PNG)|
|:--:|
| <b> Figure 3</b>|

### FAQ Page
> faq.html

Frequently asked questions can be found at this page(**Figure 4**). We are still waiting for more questions from client to add to the list. To land this page, from the navigation bar, click '?'.

|![FAQ](./readmeImages/faq.PNG)|
|:--:|
| <b> Figure 4</b>|


### Creating a study plan
The following steps outline how a user goes about the process of creating a study plan, as well as how data is processed in the background to generate the view that users end up with. 

#### Selecting a course
> 1grid-createstudyplan.html

1. Users start by selecting the course they are interested in from the first dropdown on this page. This should (Sprint 3 pending) filter the second dropdown, where users select what semester and year they wish to start studying, based on the availability of the course.
2. The semester/year start dropdown determines what the grid page (Sprint 3 pending) looks like. If a user selects a Semester 2 start, this will be reflected in the grid system. Currently, the Study Planner supports only a Semester 1, 2023 start.

The selected course and beginning year/semester gets sent via AJAX post() to *routes.py* where it is processed to determine what the next page will look like to the user (upon pressing the 'Continue' button).

#### Selecting a major or specialisation
> 2grid-createstudyplan.html

Based on what course the user selected in the previous step, this page will either appear or not appear. This is determined by whether or not the course has a major or specialisation. E.g., If a user selects the Bachelor of Commerce degree, this page will be produced with a dropdown containing 7 majors. These majors are deducted from the *Json-export.csv* file's *ListMajors* attribute. Specialisations on the other hand, are contained within the *Structure* column. If a major or specialisation is selected, it overrides the course selected in the step prior so that the correct units can be pulled based on the major/specialisation decision.

If a user would select a course that does not contain any major or specialisation, they will be redirected instantly to the page described below.

#### Selecting units
> 3grid-createstudyplan.html

This page consists of two windows. One where the user finds all unit groups and units, and one which consists of information relating to the selected course, potential major or specialisation, the faculty that heads the course and the course code, as well as the grid system.

**Unit groups and units**

On the left hand pane under the 'Select units' heading, the selected course or major/specialisation's unit group(s) (e.g., Core, Option, Conversion, etc.) and their associated units will appear. Each unit group has an information tooltip to the right of its header which, upon hover, describes the unit group based on information deducted from the *typeInto* field contained within the *Structure* attribute in *Json-export.csv*.

Each unit has a color. This color explains when it is available to study (pulls from the *Availabilities* attribute contained in *Unit list.csv*). At the bottom of the left hand pane, each key is described to the user (Semester 1 only, Semester 2 only, etc.).

Upon click of a unit, the user currently gets an alert that says what unit they have clicked on. In Sprint 3, we wish to see how we can incorporate the *Content* and *Outcomes* attributes here. This would allow the user to read about individual units.

**Grid system**
The grid system is made up of two parts. The top part provides details to the user in regard to their selected course. The second part which fills the majority of the page consists of the grid system. A layout made up of rows where each row is a semester made up of a total of 5 boxes (one box for each unit). A normal full time study load at UWA is 3-4 units, but students are allowed to overload semesters by taking a maximum of 5 units per semester.

The grid system is currently (at the end of Sprint 2) based on the HTML Drag and Drop API. This allows for units to be dragged from the unit selection pane onto a box in the grid. Clicking on the 'Add' button for a Semester row adds overloading functionality, and if the 'Add' button has been clicked, a 'Remove' button will appear to remove overloading.

Functionality on this page will (Sprint 3 pending) constrain a user's ability to drag units onto the grid based on the following rules:
* Unit group requirements
* Unit availability
* Unit co-requisites
* Unit incompatibilities
* Unit prerequisites

Additionally, this page includes functionality like saving a study plan to a user account (exclusive to authorised/logged in users) and downloading a study plan.

___

## Testing documentation

___

## Extended functionality

___

## Deployment
Deployment on localhost at port 5000, http://localhost:5000/index.
