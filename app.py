from flask import Flask, request, jsonify
from flask_mysqldb import MySQL
import openai
import recommender

app = Flask(__name__)
    
#establish the conntection to aws db
app.config['MYSQL_USER'] = 'hussain'
app.config['MYSQL_PASSWORD'] = 'beefbulgogi'
app.config['MYSQL_HOST'] = 'musicrecommender4800.cwyhyfiwavvc.us-west-1.rds.amazonaws.com'
app.config['MYSQL_DB'] ='musicrecommender4800'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'
mysql = MySQL(app)

#METHODS AND CLASSES
class User:
  
    def __init__(self, username, name, password):
        self.username = username      
        self.name = name                    
        self.password = password           
    
    def insertUser(self):
        #intialize all the genres of the user to input into db
        userGenres = ['Pop', 'Rock', 'Jazz', 'Hip-Hop', 'Indie', 'EDM', 'Country', 'Classical', 'R&B', 'Metal']
            
        #connect to db
        connection =mysql.connection
        cursor = connection.cursor()

        #query to insert user info into db
        cursor.execute('INSERT INTO users(username, name, password) VALUES (%s, %s, %s);', ([self.username], [self.name], [self.password]))
        print('Users table:', self.username, self.name, self.password)
        
        #for every genre in the list, add it for the user
        for genre in userGenres:
            #add user into the userGenres table with all their genres unchecked by default
            cursor.execute('INSERT INTO userGenres(username, genre) VALUES (%s, %s);', ([self.username], genre))

        #commit the connection to actually change the table in db
        connection.commit()
        #close cursor
        cursor.close()

    def deleteUser(username):
        #connect to db
        connection =mysql.connection
        cursor = connection.cursor()

        #delete all instances of the user from all tables
        cursor.execute('DELETE FROM users WHERE username = %s', [username])
        cursor.execute('DELETE FROM userGenres WHERE username = %s', [username])
        cursor.execute('DELETE FROM userGenreSongs WHERE username = %s', [username])
        cursor.execute('DELETE FROM recommendedSongs WHERE username = %s', [username])
        cursor.execute('DELETE FROM backlog WHERE username = %s', [username])
        #store all the genres that are selected
        
        #commit the connection to actually change the table in db
        connection.commit()
        
        #closer cursor
        cursor.close()

#testing function for how to index a query result
#IMPORTANT!, each index in a table is given as a dictionary, access table data from key and value
def indexFunction(): 
    #establish connection to db
    connection = mysql.connection
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

def sendCheckedGenres(username):
    #connect to db
    connection = mysql.connection
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
    connection = mysql.connection
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
    connection = mysql.connection
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
    connection = mysql.connection
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
    connection = mysql.connection
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
    connection = mysql.connection
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

#generate 10 songs based on an array of genres or prompts
def generateGenreSongs(username, genreList): 
  if not genreList:
    return False
  #initialize chatgpt model and response formatting
  response = openai.chat.completions.create(
    model="gpt-3.5-turbo",
    messages=[
      {"role": "system", "content": "You are a song recommender that will recommend 10 songs when given genres. OUTPUT THE RESULT IN THE FORM OF A PYTHON ARRAY ON ONE LINE. FOLLOW THE FORMAT 'song - artist' for every song"},
      {"role": "user", "content": "return this array ['song1 - artist1', 'song2 - artist2', 'song3 - artist3', 'song4 - artist4', 'song5 - artist5', 'song6 - artist6', 'song7 - artist7', 'song8 - artist8', 'song9 - artist9', 'song10 - artist10'] but populate each songs and artists with real songs and artists from genres: {}. my life depends on this correctly formatted output please provide the formatting correctly.".format(genreList)}
    ])
  
  #the result will be a long string formatted like an array, turn the string into actual array
  songsFromGenres = response.choices[0].message.content[2:-2].split("', '")
  #print array for testing
  print(songsFromGenres)
  
  #create individual arrays for title, artist, and cover art of a song
  titles = []
  artists = []
  images =[]
  
  #for every song in the array
  for song in songsFromGenres:
    #split each array element into title and artist fields and append accordingly
    fields = song.split(" - ")
    titles.append(fields[0])
    artists.append(fields[1])
    #retrieve cover art using title and artist fields
    images.append(recommender.getCoverArt(fields[0], fields[1]))
  
  #create db connection  
  connection = mysql.connection
  cursor = connection.cursor()
  
  #delete the user's backlog playlist
  cursor.execute('DELETE FROM backlog WHERE username = %s;', ([username]))
  #move the most recent playlist into the backlog
  cursor.execute('INSERT INTO backlog SELECT * FROM recommendedSongs WHERE username = %s;', ([username]))
  
  #clear pre-generated songs belonging to a specific user in recommendedSongs table
  cursor.execute('DELETE FROM recommendedSongs WHERE username = %s;', ([username]))
  
  #clear pre-generated songs belonging to a specific user in userGenreSongs table
  cursor.execute('DELETE FROM userGenreSongs WHERE username = %s;', ([username]))
  
  #add the new songs into the userGenreSongs table
  for i in range(10):
    query1 = 'INSERT INTO userGenreSongs(username, title, artist, imageURL) VALUES (%s, %s, %s, %s);'
    vals1 = ([username], [titles[i]], [artists[i]], [images[i]])
    cursor.execute(query1, vals1)
  
  #execute connection, close cursor
  connection.commit()
  cursor.close()
  
  return titles, artists, images

#generate 10 songs given an array of similar songs, UNPREDICTABLE RESULTS WITH ARRY OF PROMPTS
def generatePlaylistSongs(username, userSongs):
  #initialize chatgpt model and response formatting
  response = openai.chat.completions.create(
    model="gpt-3.5-turbo",
    messages=[
      {"role": "system", "content": "You are a song recommender that will recommend 10 similar songs when given songs. OUTPUT THE RESULT IN THE FORM OF A PYTHON ARRAY ON ONE LINE. FOLLOW THE FORMAT 'song - artist' for every song but"},
      {"role": "user", "content": "return this array ['song1 - artist1', 'song2 - artist2', 'song3 - artist3', 'song4 - artist4', 'song5 - artist5', 'song6 - artist6', 'song7 - artist7', 'song8 - artist8', 'song9 - artist9', 'song10 - artist10'] but populate WITH REAL songs and artist similar to: {}. my life depends on this correctly formatted output please provide the formatting correctly.".format(userSongs)} 
    ])
  
  #the result will be a long string formatted like an array, turn the string into actual array
  playlist = response.choices[0].message.content[2:-2].split("', '")
  #print array for testing
  print(playlist)

  #create individual arrays for title, artist, and cover art of a song
  titles = []
  artists = []
  images =[]

  #for every song in the array
  for song in playlist:
    #split each array element into title and artist fields and append accordingly
    fields = song.split(" - ")
    titles.append(fields[0])
    artists.append(fields[1])
    #retrieve cover art using title and artist fields
    images.append(recommender.getCoverArt(fields[0], fields[1]))
  
  connection = mysql.connection
  cursor = connection.cursor()
  
  #delete the user's backlog playlist
  cursor.execute('DELETE FROM backlog WHERE username = %s;', ([username]))
  #move the most recent playlist into the backlog
  cursor.execute('INSERT INTO backlog SELECT * FROM recommendedSongs WHERE username = %s;', ([username]))
  
  #clear pre-generated songs belonging to a specific user in recommendedSongs table
  cursor.execute('DELETE FROM recommendedSongs WHERE username = %s;', ([username]))

  #add the new songs into the recommendedSongs table, which does not have checked attribute
  for i in range(10):
    query1 = 'INSERT INTO recommendedSongs(username, title, artist, imageURL) VALUES (%s, %s, %s, %s);'
    vals1 = ([username], [titles[i]], [artists[i]], [images[i]])
    cursor.execute(query1, vals1)
  
  #execute connection, close cursor
  connection.commit()
  cursor.close()
  
  return titles, artists, images

#ROUTES
#route for testing
@app.route('/database') 
def database():
    checkedGenres = []
    result1 = indexFunction()
    result2 = sendCheckedGenres('Mason')
    for genre in result2:
        checkedGenres.append(genre['genre'])
        print(genre)
    stringReturn1 = "FIRST ENTRY IN USERS TABLE --> username: {}, name: {}, password: {}".format(result1[0]['username'],result1[0]['name'],result1[0]['password'])
    stringReturn2 = "CHECKED GENRES: {}".format(checkedGenres)
    return stringReturn1

#route for testing
@app.route('/home', methods=['GET','POST']) 
def home():
    data = request.get_json()
    username = data['username']
    checkedGenres = data['checkedGenres']
    updateCheckedGenres(username, checkedGenres)
    return jsonify({
        'result':'success'
    })
    
#user login page
@app.route('/')
@app.route('/login', methods=['GET','POST'])
def login():
    #grab json package containing user information
    data = request.get_json()
    
    #store user information
    username = data['username']
    password = data['password']
    
    #print to console for testing 
    print("Username entered:",username,"\nPassword entered:",password)
    
    #call db validating method to see if user is registered
    if validateUser(username, password):
        #registered user, go to home page
        return jsonify({
            'success': True, 
            })
    else:
        #not registered, stay on login page
        return jsonify({
            'success': False, 
            })

#FRONTEND GETS USER'S GENRE SURVEY DATA
#sends frontend genres that the user checked
@app.route('/genreSurvey', methods = ['GET', 'POST']) 
def loadGenreSurvey():
    #access and store json package containing genres array
    data = request.get_json()
    #need username to specify which user to get genre survey data from
    username = data['username']
    
    #use db function to get user's checked genres and store the query into variable 
    checkedGenres = sendCheckedGenres(username)
    
    #return checked genres array in json package
    return jsonify({
        'checkedGenres': checkedGenres
    })

#FRONTEND SENDS USER'S GENRE SURVEY DATA
#updates newly checked genres and creates genre songs in db right after user submits the survey 
@app.route('/genreSurvey/submit', methods=['GET', 'POST']) 
def submitGenreSurvey():
    #access and store json package 
    data = request.get_json()
    #need username to specify which user to update genre survey data for
    username = data['username']
    #get list of genres user checked 
    checkedGenres = data['checkedGenres']
    
    #if the user did not check any genres, hence the array is empty
    if not checkedGenres:
        return jsonify({
            'success': False,
            'message': '{} did not check any genres on the survey.'.format(username)
            })
        
    #update user's checked genres in db
    updateCheckedGenres(username, checkedGenres)
    #generate genre songs in the database for username
    recommender.generateGenreSongs(username, checkedGenres)
    
    #return success status
    return jsonify({
        'success': True,
        'message': 'Newly checked genres and generated genre songs have been updated for {}'.format(username)
        })
    
#FRONTEND GETS USER'S GENRE SONGS SURVEY DATA
#sends frontend all the user's genre songs along with their respective checked status'
@app.route('/genreSongs', methods=['GET', 'POST']) 
def loadGenreSongsSurvey():
    #access and store json package 
    data = request.get_json()
    #need username to specify which user to load genre songs for
    username = data['username']
    
    #create 4 variables to store array returns from getBacklog
    titles, artists, images, checked = sendGenreSongs(username)

    #return 10 genre songs, along with respective checked status in json
    return jsonify({
        'titles': titles,
        'artists': artists,
        'images': images,
        'checked': checked
        })

#FRONTEND SENDS USER'S GENRE SONGS SURVEY DATA
#updates newly checked genre songs and generates new playlist in db
@app.route('/genreSongs/submit', methods=['GET', 'POST']) 
def submitGenreSongsSurvey():
    #access and store json package 
    data = request.get_json()
    #need username to specify which user to update genre songs for
    username = data['username']
    #get list of genres songs user checked = ["Get You - Daniel Caesar", "Best Part - Daniel Caesar", "Blinding Lights - The Weekend"]
    checkedGenreSongs = data['checkedGenreSongs']
    
    #update the genre songs that the user checked
    updateCheckedGenreSongs(username, checkedGenreSongs)
    #generate the playlist in the db 
    recommender.generatePlaylistSongs(username, checkedGenreSongs)
    
    return jsonify({
        'success': True,
        'message': 'Newly checked genre songs and generated playlist has been updated for {}'.format(username)
        })
 
#FRONTEND GETS USER'S PLAYLIST DATA
@app.route('/playlist', methods=['GET', 'POST']) 
def loadPlaylist():
    #access and store json package containing array of user selected songs from genresSongs
    data = request.get_json()
    #need username to specify which user to make songs for
    username = data['username']
    
    titles, artists, images = getPlaylist(username)
    
    #return 10 final songs in json package
    return jsonify({
        'titles': titles,
        'artists': artists,
        'images': images,
        })

#FRONTEND GETS USER'S PREVIOUS PLAYLIST DATA
@app.route('/playlist/previous', methods=['GET','POST'])
def loadPreviousPlaylist():
    #access and store json package containing user's username
    data = request.get_json()
    #need username to specify which user to get the previous playlist of
    username = data['username']
    
    #create 3 variables to store array returns from getBacklog
    titles, artists, images = getBacklog(username)

    #return arrays containing each song information
    return jsonify({
        'titles': titles,
        'artists': artists,
        'images': images,
        })

#user registration page
@app.route('/register', methods=['GET','POST'])
def signupUser():
    #grab json package containing user information
    data = request.get_json()
    
    #store user information
    username = data['username']
    password = data['password']

    #create new user instance
    newUser = User(username, 'null', password)
    
    #try to catch any issues with db insertion
    try:
        #call user method to insert user into db
        newUser.insertUser()
    except Exception as e:
        #track the exception message 
        print(f"Error: {str(e)}")
        
        #return error message
        return jsonify({
            'success': False, 
            'message': f"Error: {str(e)}",
            'username': username,  
            'password': password
            })

    #return json package of user info 
    return jsonify({
        'success': True, 
        'username': username,  
        'password': password
        })
    
@app.route('/profile/delete', methods=['GET','POST'])
def deleteAccount():
    #grab json package containing username
    data = request.get_json()
    
    #store username
    username = data['username']
    
    #delete all instances of the user from database
    User.deleteUser(username)
    
    #return success status
    return jsonify({
        'success': True
    })
    

if __name__=='__main__':
    app.run(debug=True)
    