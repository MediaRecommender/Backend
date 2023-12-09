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

def sendCheckedGenres(username):
    #connect to db
    connection = connectDB().connection
    cursor = connection.cursor()

    #query for all the genres belonging to user that are checked
    cursor.execute('SELECT genre FROM userGenres WHERE username = %s AND checked = 1;', [username])
    
    #store all the genres that are selected
    query = cursor.fetchall()
    
    #create array to return list of user's checked genres in survey
    checkedGenres = []
    
    #append each genre into array
    for genre in query:
        checkedGenres.append(genre['genre'])
        print(genre)
    
    #closer cursor
    cursor.close()
    
    return checkedGenres
    
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

def sendGenreSongs(username):
    #connect to db
    connection = connectDB().connection
    cursor = connection.cursor()

    #query for all the genre songs belonging to user
    cursor.execute('SELECT * FROM userGenreSongs WHERE username = %s;', [username])
    
    #store all the genre songs that are selected
    genreSongs = cursor.fetchall()
    
    #create arrays to store each detail of a song
    titles = []
    artists = []
    images = []
    checked = []
    
    #insert information into arrays
    for song in genreSongs:
        titles.append(song['title'])
        artists.append(song['artist'])
        images.append(song['imageURL'])
        checked.append(song['checked'])
        
    #closer cursor
    cursor.close()
    
    #return 3 arrays for the titless, artists, and imageURLs
    return (titles, artists, images, checked)
    
#checkedGenreSongsList = ["Get You - Daniel Caesar", "Best Part - Daniel Caesar", "Blinding Lights - The Weekend"]
def updateCheckedGenreSongs(username, checkedGenreSongsList):
    #connect to db
    connection = connectDB().connection
    cursor = connection.cursor()
    
    #create array for only storing song titles
    titles = []
    
    #append each title into the array
    for titleAndArtist in checkedGenreSongsList:
        titles.append(titleAndArtist.split(" - ")[0])

    #set checked status to false for respective genres in db
    cursor.execute('UPDATE userGenreSongs SET checked = 0 WHERE username = %s;', [username])
    
    #set checked status to true for only for those in checkedSongsList
    for title in titles:
        cursor.execute('UPDATE userGenreSongs SET checked = 1 WHERE title = %s AND username = %s;', ([title], [username]))
        print('Checked:', title)
        
    #commit the connection to actually change the table in db
    connection.commit()
    #close cursor
    cursor.close()

def getPlaylist(username):
    #connect to db
    connection = connectDB().connection
    cursor = connection.cursor()

    #query for all the playlist songs belonging to user
    cursor.execute('SELECT * FROM recommendedSongs WHERE username = %s;', [username])
    
    #store all the backlogged songs that are selected
    playlist = cursor.fetchall()
    
    #create arrays to store each detail of a song
    titles = []
    artists = []
    images = []
    
    #insert information into arrays
    for song in playlist:
        titles.append(song['title'])
        artists.append(song['artist'])
        images.append(song['imageURL'])
        
    #closer cursor
    cursor.close()
    
    #return 3 arrays for the titless, artists, and imageURLs
    return (titles, artists, images)
    
def getBacklog(username):
    #connect to db
    connection = connectDB().connection
    cursor = connection.cursor()

    #query for all the songs belonging to user that are checked
    cursor.execute('SELECT * FROM backlog WHERE username = %s;', [username])
    
    #store all the backlogged songs that are selected
    previousPlaylist = cursor.fetchall()
    
    #create arrays to store each detail of a song
    titles = []
    artists = []
    images = []
    
    #insert information into arrays
    for song in previousPlaylist:
        titles.append(song['title'])
        artists.append(song['artist'])
        images.append(song['imageURL'])
        
    #closer cursor
    cursor.close()
    
    #return 3 arrays for the titless, artists, and imageURLs
    return (titles, artists, images)

    
  
    
