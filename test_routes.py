import unittest
from app import app

class FlaskTestCase(unittest.TestCase):

    # Ensure that Flask was set up correctly
    def test_index(self):
        tester = app.test_client(self)
        response = tester.get('/', content_type='html/text')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'GAIN AN EXPERIENCE RICH EDUCATION', response.data)
        self.assertIn(b'Ready to Plan your', response.data)
        self.assertIn(b'future at UWA?', response.data)

if __name__ == '__main__':
    unittest.main()