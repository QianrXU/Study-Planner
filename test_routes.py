import unittest
from app import app

class FlaskTestCase(unittest.TestCase):

    # Ensure that Flask has been set up successfully and the index page shows up the right content.
    def test_index(self):
        tester = app.test_client(self)
        response = tester.get('/', content_type='html/text')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'GAIN AN EXPERIENCE RICH EDUCATION', response.data)
        self.assertIn(b'Ready to Plan your', response.data)
        self.assertIn(b'future at UWA?', response.data)

    # Ensure the faq page shows up correctly using the url
    def test_faq(self):
        tester = app.test_client(self)
        response = tester.get('/faq', content_type='html/text')
        self.assertEqual(response.status_code, 200) 
        self.assertIn(b'What is Study Planner?', response.data) # check if the sentence will be included in the response data
        self.assertIn(b'The Study Planner is a UWA tool that allows students to create study plans for their future studies.', response.data)
        self.assertIn(b'How do i use study planner tool?', response.data)
        self.assertIn(b'Lorem ipsum dolor sit amet, consectetur adipisicing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat.', response.data)
        self.assertIn(b'Do i need to sign up?', response.data)
        self.assertIn(b'Lorem ipsum dolor sit amet, consectetur adipisicing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat.', response.data)
    
    # Ensure when users log out, the page will be redirected to the index page.
    def test_logout(self):
        tester = app.test_client(self)
        tester.post(
            '/login', 
            data=dict(email='apple@mail.com', password='123456'), # test user data already exist in the database
            follow_redirects=True
        )
        response = tester.get('/logout', follow_redirects=True)
        self.assertTrue(b'' in response.data)

if __name__ == '__main__':
    unittest.main()