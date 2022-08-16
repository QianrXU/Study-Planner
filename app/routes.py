from app import app
from flask import render_template

@app.route('/', methods=['GET', 'POST'])
def index():
    return "Hello World!"

# wait till pages to be ready to add more routes
# @app.route('/signup', methods=['GET', 'POST'])
# def signup():
#    return render_template('signup.html')

if __name__ == '__main__':
   app.run(debug = True)
# Login Page
@app.route('/login', methods=['GET', 'POST'])
def login():
 
        

    return render_template('login.html', title="Log In")

