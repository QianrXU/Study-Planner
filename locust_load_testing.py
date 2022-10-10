import time
from locust import HttpUser, between, task


class MyWebsiteUser(HttpUser):
  wait_time = between(5, 15)

  @task
  def load_index(self):
    self.client.get("/")

  @task
  def load_signup(self):
    self.client.get(url="/signup")

  @task
  def load_login(self):
    self.client.get(url="/login")

  @task
  def load_faq(self):
    self.client.get(url="/faq")
  
  # task failure, need to modify
  @task
  def load_account(self):
    self.client.get(url="/account")

  @task
  def load_courses(self):
    self.client.get(url="/createstudyplan-courses")

  # task failure, need to modify
  @task
  def load_majors(self):
    self.client.get(url="/createstudyplan-majors")

  # task failure, need to modify
  @task
  def load_units(self):
    self.client.get(url="/createstudyplan-units")
