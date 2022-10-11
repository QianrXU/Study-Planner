import unittest
from app import app

class FlaskTestCase(unittest.TestCase):

    # Ensure that Flask has been set up successfully and the index page shows up the right content.
    def test_index(self):
        tester = app.test_client(self)
        # this will get the index url and retrieve an html content
        response = tester.get('/', content_type='html/text')
        # compare the status code we get from the response with the status code we should have 
        self.assertEqual(response.status_code, 200)

    # Ensure the faq page shows up correctly using the url
    def test_faq(self):
        tester = app.test_client(self)
        # this will get the faq url and retrieve an html content
        response = tester.get('/faq', content_type='html/text')
        # compare the status code we get from the response with the status code we should have 
        self.assertEqual(response.status_code, 200) 
    
    
    # Ensure a 404 page will return when a page is not found.
    def test_page_not_found(self):
        tester = app.test_client(self)
        # this will get the somepage url not included in the routes we have and retrieve an html content
        response = tester.get('/somepage', content_type='html/text')
        # compare the status code we get from the response with the status code we should have 
        self.assertEqual(response.status_code, 404)

    # Test if the signup page can be rendered successfully.
    def test_loading_signup(self):
        tester = app.test_client(self)
        # this will get the signup url and retrieve an html content
        response = tester.get('/signup', content_type='html/text')
        # compare the status code we get from the response with the status code we should have 
        self.assertEqual(response.status_code, 200)

    # Test if the login page can be rendered successfully.
    def test_loading_login(self):
        tester = app.test_client(self)
        # this will get the login url and retrieve an html content
        response = tester.get('/login', content_type='html/text')
        # compare the status code we get from the response with the status code we should have 
        self.assertEqual(response.status_code, 200)
    
    # Ensure when users log out, the page will be redirected to the index page.
    def test_logout(self):
        tester = app.test_client(self)
        # use some test data to login
        tester.post(
            '/login', 
            data=dict(email='apple@mail.com', password='123456'), 
            follow_redirects=True
        )
        # the page should be redirected when the logout url is reached
        response = tester.get('/logout', follow_redirects=True) 
        # There should be no message shown when users log out
        self.assertTrue(b'' in response.data) 

    # Needs modifications: right now the status_code is 500 rather than 200
    def test_account(self):
        tester = app.test_client(self)
        tester.post(
            '/login', 
            data=dict(email='apple@mail.com', password='123456'), 
            follow_redirects=True
        )
        response = tester.get('/account', content_type='html/text')
        self.assertEqual(response.status_code, 200)
    
    # Ensure users can get to the course selection page
    def test_loading_course_selection(self):
        tester = app.test_client(self)
        tester.post(
            '/createstudyplan-courses', 
            data=dict(selectedCourse='master of IT', selectedStart='semester 2, 2023'), 
            follow_redirects=True
        )
        # this will get the login url and retrieve an html content
        response = tester.get('/createstudyplan-courses', content_type='html/text')
        # compare the status code we get from the response with the status code we should have 
        self.assertEqual(response.status_code, 200)

    # returns a 404 at the moment
    def test_loading_major_selection(self):
        tester = app.test_client(self)
        tester.post(
            '/createstudyplan-majors', 
            data=dict(selectedMajor='software engineering specialisation'), 
            follow_redirects=True
        )
        # this will get the login url and retrieve an html content
        response = tester.get('/createstudyplan-majors', content_type='html/text')
        # compare the status code we get from the response with the status code we should have 
        self.assertEqual(response.status_code, 200)

    # returns a 404 at the moment
    def test_loading_unit_selection(self):
        tester = app.test_client(self)
        # this will get the login url and retrieve an html content
        response = tester.get('/createstudyplan-units', content_type='html/text')
        # compare the status code we get from the response with the status code we should have 
        self.assertEqual(response.status_code, 200) 

if __name__ == '__main__':
    unittest.main()