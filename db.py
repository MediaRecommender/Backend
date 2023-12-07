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
    
def updateCheckedGenres(username, checkedGenresList):
    #connect to db
    connection = connectDB().connection
    cursor = connection.cursor()

    #set checked status to false for respective genres in db
    cursor.execute('UPDATE userGenres SET checked = 0 WHERE username = %s;', [username])
    
    #set checked status to true for only for those in checkedGenresList
    for genre in checkedGenresList:
        cursor.execute('UPDATE userGenres SET checked = 1 WHERE genre = %s AND username = %s;', ([genre], [username]))
        print('Checked:', genre)
        
    #commit the connection to actually change the table in db
    connection.commit()
    #close cursor
    cursor.close()

def sendCheckedGenres(username):
    #connect to db
    connection = connectDB().connection
    cursor = connection.cursor()

    #query for all the genres belonging to user that are checked
    cursor.execute('SELECT genre FROM userGenres WHERE username = %s AND checked = 1;', [username])
    
    #store all the genres that are selected
    results = cursor.fetchall()
    
    #closer cursor
    cursor.close()
    
    return results

def updateCheckedSongs(username, checkedSongsList):
    #create array to store only titles
    titles = []
    
    #append only the title of each song into titles array
    for song in checkedSongsList:
        titleAndArtist = song.split(" - ")
        titles.append(titleAndArtist[0])

    #connect to db
    connection = connectDB().connection
    cursor = connection.cursor()

    #set checked status to false for respective genres in db
    cursor.execute('UPDATE userGenreSongs SET checked = 0 WHERE username = %s;', [username])
    
    #set checked status to true for only for those in checkedSongsList
    for song in titles:
        cursor.execute('UPDATE userGenreSongs SET checked = 1 WHERE title = %s AND username = %s;', ([song], [username]))
        print('Checked:', song)
        
    #commit the connection to actually change the table in db
    connection.commit()
    #close cursor
    cursor.close()
    
def sendCheckedSongs(username):
    #connect to db
    connection = connectDB().connection
    cursor = connection.cursor()

    #query for all the songs belonging to user that are checked
    cursor.execute('SELECT title FROM recommendedSongs WHERE username = %s AND checked = 1;', [username])
    
    #store all the genres that are selected
    results = cursor.fetchall()
    
    #closer cursor
    cursor.close()
    
    return results
    
