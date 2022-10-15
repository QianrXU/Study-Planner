# Adapted codes based on: https://github.com/nicolaigram/loadtesting_locustio/blob/main/basic_load_testing/locust.py

import time
from locust import HttpUser, between, task


class MyWebsiteUser(HttpUser):
  wait_time = between(5, 15)

  @task(1)
  def load_index(self):
    # test the GET request of index page
    self.client.get("/")

  @task
  def load_signup(self):
    # test the GET request of signup page
    self.client.get(url="/signup")
    # test the POST request of signup page
    self.client.post(url="/signup", json={'email':'test@gmail.com', 'password':'password', 'password2':'password'})

  @task
  def load_login(self):
    # test the GET request of login page
    self.client.get(url="/login")
    # test the POST request of login page
    self.client.post(url="/login", json={'email':'test@gmail,com', 'password':'password'})

  @task
  def load_faq(self):
    # test the GET request of faq page
    self.client.get(url="/faq")
  
  # need to add login into the process?
  @task
  def load_account(self):
    # test the GET request of login page
    self.client.get(url="/account")

  @task(2)
  def load_courses(self):
    # test the GET request of course selection page
    self.client.get(url="/createstudyplan-courses")
    # test the POST request of course selection page, FAILED WITH 500
    self.client.post("/createstudyplan-courses", json={"selectedCourse": "Master of Professional Engineering", "selectedStart": "Semester 1, 2023"})

  # task failure, need to modify
  @task(3)
  def load_majors(self):
    # test the GET request of major selection page, FAILED WITH 500
    self.client.get(url="/createstudyplan-majors")
    # test the POST request of major selection page, FAILED WITH 500
    self.client.post("/createstudyplan-majors", json={"selectedMajor": "Software Engineering Specialisation"})

  # task failure, need to modify
  @task(4)
  def load_units(self):
    # test the GET request of units selection page, FAILED WITH 500
    self.client.get(url="/createstudyplan-units")
    # test the POST request of major selection page, do it after the errors above have been fixed
