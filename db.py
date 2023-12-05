from flask import Flask
from flask_mysqldb import MySQL
from app import app

#method to avoid repeption when conntecting db and cursor
def connectDB():
    mysql = MySQL(app)
    return mysql

#testing function for how to index a query result
#IMPORTANT!, each index in a table is given as a dictionary, access table data from key and value
def indexFunction(): 
    #establish connection to db
    connection = connectDB().connection
    cursor = connection.cursor()

    #run a query 
    cursor.execute('SELECT * FROM users;')
    #store query into variable
    results = cursor.fetchall()

    #close cursor
    cursor.close()

    return results

def validateUser(username,password):
    #establish connection to db
    connection = connectDB().connection
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
    
    
