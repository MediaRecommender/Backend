from flask import Flask
from flask_mysqldb import MySQL

#method to avoid repeption when conntecting db and cursor
def connectDB():
    from app import app, mysql
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

def validateUser(email,password):
    #establish connection to db
    connection = connectDB().connection
    cursor = connection.cursor()
    
    #execute query to select password belonging to email user entered, if it is a registered email
    cursor.execute('SELECT password FROM users WHERE email LIKE %s', [email])
    #store query result to variable, which should be a key value pair 
    queryResult = cursor.fetchone()

    #close cursor
    cursor.close()

    #if email is registered,
    if queryResult is not None:
        print("Query Result:",queryResult)
        #store the associated password of email to variable
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
    

