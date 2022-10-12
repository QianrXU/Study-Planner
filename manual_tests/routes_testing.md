## Routes Testing

### Introduction 
Unit tests on the routes have been written on this file: [test_routes.py](https://github.com/QianrXU/Study-Planner/blob/main/test_routes_valerie.py). 
Routes that have been tested are as follows:
- / (index) 
- /signup
- /login
- /account
- /logout
- /faq
- page_not_found
- /createstudyplan-courses
- /createstudyplan-majors
- /createstudyplan-units

### Results
The result of running the tests in the file should be:
```
test_faq (test_routes.FlaskTestCase) ... ok
test_account (test_routes.FlaskTestCase) ... ok
test_index (test_routes.FlaskTestCase) ... ok
test_loading_course_selection (test_routes.FlaskTestCase) ... ok
test_loading_login (test_routes.FlaskTestCase) ... ok
test_loading_major_selection (test_routes.FlaskTestCase) ... ok
test_loading_signup (test_routes.FlaskTestCase) ... ok
test_loading_unit_selection (test_routes.FlaskTestCase) ... ok
test_logout (test_routes.FlaskTestCase) ... ok
test_page_not_found (test_routes.FlaskTestCase) ... ok



----------------------------------------------------------------------
Ran 10 tests in 0.296s



OK
```

## Load Testing

### Introduction 
The loading tests are done on Locust.io, which is a scriptable and scalable performance testing tool. The loading tests can be found on this file: [locust_load_testing.py](https://github.com/QianrXU/Study-Planner/blob/main/locust_load_testing.py). 
POST requests and GET requests have been tested on the following routes:
- / (index)
- /account
- /createstudyplan-courses
- /createstudyplan-majors
- /createstudyplan-units
- /faq
- /login
- /singup	


### Results
#### Loading tests with 50 users
![total_requests_per_second_1665543658](https://user-images.githubusercontent.com/83133588/195239926-63eb9bbc-0128-4764-b5a0-66996e3dfcf6.png)
![response_times_(ms)_1665543658](https://user-images.githubusercontent.com/83133588/195239933-9428c289-8043-4ab7-a618-371b24fe9732.png)
![number_of_users_1665543658](https://user-images.githubusercontent.com/83133588/195239946-d66255df-5c61-4f94-9832-12bf0b0e98d2.png)

#### Loading tests with 100 users
![total_requests_per_second_1665543706](https://user-images.githubusercontent.com/83133588/195240028-ae5af554-94f2-42a5-9818-a0376311cabd.png)
![response_times_(ms)_1665543707](https://user-images.githubusercontent.com/83133588/195240043-342bab28-3bb7-4260-83c9-42dcac49cdcb.png)
![number_of_users_1665543707](https://user-images.githubusercontent.com/83133588/195240052-a7d485aa-c72b-40bf-a753-5e2c2a2962df.png)

#### Loading tests with 300 users
![total_requests_per_second_1665543738](https://user-images.githubusercontent.com/83133588/195240151-f093d554-3f5d-4a48-8cd6-7e990d226b38.png)
![response_times_(ms)_1665543738](https://user-images.githubusercontent.com/83133588/195240159-59e3681b-b822-4235-a7ea-3d2b33cf4e40.png)
![number_of_users_1665543738](https://user-images.githubusercontent.com/83133588/195240168-aff54768-15e2-4049-85b4-ae5005cdb284.png)

