# Tests Related to User Interface

## Routes Testing

### Introduction 
Database tests have been written on this file:[database_test.py] that can be found in the same folder.
More information regarding to database can be found in [README.md]
### Content
The feature that has been tested are:

## Creation of Tables
(1) User Table creation
(2) Four__Sem_SP Table creation

## Schema of Tables
(1) User Table Schema
(2) Four__Sem_SP Table Schema

## Transaction Testing
(1) Addition for User table
(2) Deletion for User Table
(3) Addition for Four__Sem_SP table
(4) Deletion for Four__Sem_SP Table


### Results

## Creation of Tables
user table has been created
studyplan table has been created

## Schema of Tables
Schema of User Table is correct
Schema of Four Semester Study Plan Table is correct

## Transaction Testing
Unable to add data to User table
Able to delete data from User table :)
Able to add data to Four Semester Study Plan table :)
Able to delete data from Four Semester Study Plan table :)

The reason that it is not able to add data through database to the user table is because that all the password are encrypted and recorded in the table as password_hash instead of password.