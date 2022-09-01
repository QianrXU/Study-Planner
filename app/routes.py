from app import app
from flask import render_template, redirect, url_for
from flask_login import current_user, login_user, logout_user, login_required

@app.route('/')
@app.route('/index', methods=['GET', 'POST'])
def index():
    return render_template('index.html', title='Home')

<<<<<<< HEAD


@app.route('/signUp', methods=['GET', 'POST'])
def signUp():
    return render_template('signUp.html')
=======
# Signup Page
@app.route('/signup', methods=['GET', 'POST'])
def signup():
    """
    message = ''
        if request.method == 'POST' and 'name' in request.form and 'password' in request.form and 'email' in request.form :
            userName = request.form['name']
            password = request.form['password']
            email = request.form['email']
            cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            cursor.execute('SELECT * FROM user WHERE email = % s', (email, ))
            account = cursor.fetchone()
            if account:
                message = 'Account already exists !'
            elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
                message = 'Invalid email address !'
            elif not userName or not password or not email:
                message = 'Please fill out the form !'
            else:
                cursor.execute('INSERT INTO user VALUES (NULL, % s, % s, % s)', (userName, email, password, ))
                mysql.connection.commit()
                message = 'You have successfully registered !'
        elif request.method == 'POST':
            message = 'Please fill out the form !'
    """
    return render_template('signUp.html', title='Sign Up')
>>>>>>> 0b39856f78242424897aa0dc7207a7bdc90f4dd4

# Login Page
@app.route('/login', methods=['GET', 'POST'])
def login():
    """
    message = ''
        if request.method == 'POST' and 'email' in request.form and 'password' in request.form:
            email = request.form['email']
            password = request.form['password']
            cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            cursor.execute('SELECT * FROM user WHERE email = % s AND password = % s', (email, password, ))
            user = cursor.fetchone()
            if user:
                session['loggedin'] = True
                session['userid'] = user['userid']
                session['name'] = user['name']
                session['email'] = user['email']
                message = 'Logged in successfully !'
                return render_template('user.html', mesage = mesage)
            else:
                message = 'Please enter correct email / password !'
    """
    return render_template('login.html', title="Log In")

"""
# logout the user and redirect to index page
@app.route('/logout', methods=['GET', 'POST'])
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))
"""

# Account Page
@app.route('/myaccount', methods=['GET', 'POST'])
def account():
    return render_template('myaccount.html', title="My Account")


# Studyplanner step 1
@app.route('/createstudyplan-courses', methods=['GET', 'POST'])
def createstudyplanstep1():
    return render_template('step1-createstudyplan.html', title="Create study plan")

# Studyplanner step 2
@app.route('/home', methods=['GET', 'POST'])
def home():
    return render_template('home.html', title="home")

#faq
@app.route('/faq', methods=['GET', 'POST'])
def faq():
    return render_template('faq.html', title="FAQ")


# Download PDF
@app.route('/pdf', methods=['GET', 'POST'])
def download():
    return render_template('get_pdf.html', title="PDF")

# FAQ Page
@app.route('/faq', methods=['GET', 'POST'])
def faq():
    return render_template('faq.html', title="FAQ")

# 404 Page
@app.errorhandler(404)
def page_not_found(e):
<<<<<<< HEAD
    return render_template('signUp.html'), 404
=======
    return render_template('404.html'), 404

if __name__ == '__main__':
    app.run(debug=True)
>>>>>>> 0b39856f78242424897aa0dc7207a7bdc90f4dd4
