from flask import Flask, request, redirect, render_template, url_for, jsonify
from flask_mysqldb import MySQL
import requests
import recommender

app = Flask(__name__)
    
#establish the conntection to aws db
app.config['MYSQL_USER'] = 'hussain'
app.config['MYSQL_PASSWORD'] = 'beefbulgogi'
app.config['MYSQL_HOST'] = 'musicrecommender4800.cwyhyfiwavvc.us-west-1.rds.amazonaws.com'
app.config['MYSQL_DB'] ='musicrecommender4800'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'
mysql = MySQL(app)

class User:
    def __init__(self, username, name, password):
        self.username = username      
        self.name = name                    
        self.password = password           
    
    def insertUser(self):
        try:
            #Connect to db
            connection = mysql.connection
            cursor = connection.cursor()

            #query to user info into database
            query = 'INSERT INTO users(username, name, password) VALUES (%s, %s, %s);'
            vals = (self.username, self.name, self.password)
            print(vals)

            #execut the query 
            cursor.execute(query, vals)

            #coomit the connection to actually change the table in db
            connection.commit()
            #close cursor
            cursor.close()

        except Exception as e:
            print(f"Error: {str(e)}")

def validateUser(username,password):
    #establish connection to db
    connection = mysql.connection
    cursor = connection.cursor()
    
    #execute query to select password belonging to username user entered, if it is a registered username
    cursor.execute('SELECT password FROM users WHERE username LIKE %s', [username])
    #store query result to variable, which should be a key value pair 
    queryResult = cursor.fetchone()

    #close cursor
    cursor.close()

    #if username is registered,
    if queryResult is not None:
        print("Query Result:",queryResult)
        #store the associated password of username to variable
        registeredPassword = queryResult.get('password')  

        #if the passwords match up, return true
        if password == registeredPassword:     
            return True
        else:
            #if user entered incorrect password
            return False
    #if not registered.
    else:
        return False

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
    if validateUser(username, password):
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