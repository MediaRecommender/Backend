<<<<<<< HEAD
from flask import Flask, render_template, url_for

from flask_login import UserMixin

from flask_sqlalchemy import *

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI']='postgresql://cs4800admin:password@musicrecommender-db.cqcweq8o7ffq.us-east-2.rds.amazonaws.com/postgres'
db = SQLAlchemy(app)




@app.route('/')
def home():
    return render_template('home.html')
=======
from flask import Flask, request, redirect, render_template, url_for
from flask_mysqldb import MySQL
from user import User
import db

app = Flask(__name__)

#establish the conntection to aws db
app.config['MYSQL_USER'] = 'admin'
app.config['MYSQL_PASSWORD'] = 'password'
app.config['MYSQL_HOST'] = 'musicrecommender-db.cwyhyfiwavvc.us-west-1.rds.amazonaws.com'
app.config['MYSQL_DB'] ='musicrecommender'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'
mysql = MySQL(app)

#route is just for testing db functions
@app.route('/database')
def database():
    result = db.indexFunction()
    stringReturn = "FIRST ENTRY IN USERS TABLE --> email: {}, name: {}, password: {}".format(result[0]['email'],result[0]['name'],result[0]['password'])
    return stringReturn

@app.route('/home')
def home():
    return render_template('home.html')

@app.route('/')
>>>>>>> main
@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/register')
def register():
    return render_template('register.html')

<<<<<<< HEAD
=======
#POST method means expecting data back from user
@app.route('/register', methods=['POST'])
def signup_user():
    #create new user instance. use request.form.get to grab user data from register html page
    newUser = User(
        email=request.form.get('email'),
        name=request.form.get('name'),
        password=request.form.get('password'),
    )
    #call user method to insert user into db
    newUser.insertUser()
    return redirect(url_for('home'))

@app.route('/login', methods=['POST'])
def loginUser():
    #grab user data from login html page
    email = request.form.get('email')
    password = request.form.get('password')

    #print to console for testing 
    print("Email entered:",email,"\nPassword entered:",password)

    #call db validating method to see if user is registered
    if db.validateUser(email, password):
        #registered user, go to home page
        return redirect(url_for('home'))
    else:
        #not registered, stay on login page
        return redirect(url_for('login'))
>>>>>>> main

if __name__=='__main__':
    app.run(debug=True)