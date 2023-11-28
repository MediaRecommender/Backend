from flask import Flask, render_template, url_for

from flask_login import UserMixin

from flask_sqlalchemy import *

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI']='postgresql://cs4800admin:password@musicrecommender-db.cqcweq8o7ffq.us-east-2.rds.amazonaws.com/postgres'
db = SQLAlchemy(app)




@app.route('/')
def home():
    return render_template('home.html')
@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/register')
def register():
    return render_template('register.html')


if __name__=='__main__':
    app.run(debug=True)