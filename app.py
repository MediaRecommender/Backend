from flask import Flask, request, redirect, render_template, url_for, jsonify
from flask_mysqldb import MySQL
import requests
from user import User
import db
import recommender

app = Flask(__name__)
    
#establish the conntection to aws db
app.config['MYSQL_USER'] = 'hussain'
app.config['MYSQL_PASSWORD'] = 'beefbulgogi'
app.config['MYSQL_HOST'] = 'musicrecommender4800.cwyhyfiwavvc.us-west-1.rds.amazonaws.com'
app.config['MYSQL_DB'] ='musicrecommender4800'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'
mysql = MySQL(app)

#route is just for testing db functions
@app.route('/database')
def database():
    result = db.indexFunction()
    stringReturn = "FIRST ENTRY IN USERS TABLE --> username: {}, name: {}, password: {}".format(result[0]['username'],result[0]['name'],result[0]['password'])
    return stringReturn

@app.route('/home')
def home():
    return render_template('home.html')

@app.route('/')
@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/register')
def register():
    return render_template('register.html')

@app.route('/survey')
def survey():
    return render_template('survey.html')

#POST method means expecting data back from user
@app.route('/register', methods=['POST'])
def signupUser():
    #use request.form.get to grab user data from register html page
    username=request.form.get('email')
    name=request.form.get('name')
    password=request.form.get('password')

    #create new user instance
    newUser = User(username, name,password)
    #call user method to insert user into db
    newUser.insertUser()

    #return json package of user info 
    return redirect(url_for('home'))
    return jsonify({
        'success': True, 
        'username': username,  
        'name':name, 
        'userPassword': password
        })

@app.route('/login', methods=['POST'])
def loginUser():
    #grab user data from login html page
    username = request.form.get('email')
    password = request.form.get('password')
    #print to console for testing 
    #print("Username entered:",username,"\nPassword entered:",password)
    #call db validating method to see if user is registered
    if db.validateUser(username, password):
        #registered user, go to home page
        #return redirect(url_for('survey'))
        return jsonify({
            'success': True, 
            'message': 'Welcome!'
            })
    else:
        #not registered, stay on login page
        #return redirect(url_for('login'))
        return jsonify({
            'success': False, 
            'message': 'Invalid username or password!'
        })

if __name__=='__main__':
    app.run(debug=True)