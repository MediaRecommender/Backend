from flask import Flask, request, redirect, render_template, url_for
from flask_mysqldb import MySQL
from user import User
import db
import openai
openai.api_key = "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"

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
@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/register')
def register():
    return render_template('register.html')

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
    
def recommendedMusic(song1, song2, song3, song4, song5):
    response = openai.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a music recommender system that will " +
            "return 5 similar songs along with their respective artist names and cover art jpeg" +
            "links in the form of a python dictionary when given a couple of song names"},
            {"role": "user", "content": "return 5 similar songs along with their respective artist " +
             "names and cover art jpeg links for the songs in the form of a python dictionary: {}, {}, {}, {}, {}".format(song1,song2,song3,song4,song5)}
        ]
    )
    print(response.choices[0].message)
    return response.choices[0].message

if __name__=='__main__':
    app.run(debug=True)