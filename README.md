# Study Planner (Team 1)
This is the main repository and project planning page of Study Planner Team 1 (part of CITS5206 Professional Computing).

___

## User Manual
* Project Details 
* How to Run the Project
* Database Schema
* Functionalities
  * Sign up
  * Log in
  * Select units
  * Save study plan
  * Download study plan
* Testing documentations
* Extended Functions for Final Project

___

## Project Details
A study plan helps students to plan their sequence of units for a university course such as the Masters of IT. Currently, study plans are created by hand based on the unit sequence, course rules, and semester availability, which are stored in UWAs CAIDi curriculum management system. This project aims to automate the process of building a study plan for a given UWA course. 

The Study Planner software will: 
*Given a University program exported from CAIDi, automatically create a feasible study plan for students starting either in semester 1 or 2 satisfying given constraints on a course (core units, prerequisites, semester availability) 
*Provide an interactive visualisation of a given study plan, enabling students and staff to explore study plan options and visualise constraints on the plan 
*Allow students or staff to propose adjustments to a study plan such as the addition or deletion of units 
*Allow students or staff to download a completed study plan and upload an existing plan to make changes 

This application is using flask as the backend framework and its FlaskSQLAlchemy for the database.

___

## How to run the project (Unix)
**Step 1**
* Use pip or another package manager to install virtualenv package: `$ sudo apt-get install python3-venv`

**Step 2**
1. Create a virtual environment: `$ python3 -m venv venv`
2. Activate the python virtual environment: `$ source venv/bin/activate`
3. Install prerequisites (requires python3, flask, venv, etc.): `$ pip3 install -r requirements.txt`.
4. To run the app: `$ flask run` - This should start the app running on localhost at port 5000, i.e.  http://localhost:5000/index
5. To stop the app: `$ ^C`
6. To exit the environment: `$ deactivate`

## How to run the project (Windows)
**Step 1**
* Use pip or another package manager to install virtualenv package: `$ xxxxx`

**Step 2**
1. Create a virtual environment: `$ python3 -m venv venv`
2. Activate the python virtual environment: `$ source venv\Scripts\activate`
3. Install prerequisites (requires python3, flask, venv, etc.): `$ xxxxx`.
4. To run the app: `$ flask run` - This should start the app running on localhost at port 5000, i.e.  http://localhost:5000/index
5. To stop the app: `$ ^C`
6. To exit the environment: `$ deactivate`
___

## Database Schema

___


## Functionalities

___


## Testing Documentations

___


## Extended Functions for Final Project

___

## Deployment
Deployment on localhost at port 5000.
