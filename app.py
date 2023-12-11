from flask import Flask, request, jsonify
from flask_mysqldb import MySQL
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

#route for testing
@app.route('/database') 
def database():
    checkedGenres = []
    result1 = db.indexFunction()
    result2 = db.sendCheckedGenres('Mason')
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
    db.updateCheckedGenres(username, checkedGenres)
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
    if db.validateUser(username, password):
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
    checkedGenres = db.sendCheckedGenres(username)
    
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
    db.updateCheckedGenres(username, checkedGenres)
    #generate genre songs in the database for username
    flag = recommender.generateGenreSongs(username, checkedGenres)
    while (not flag):
        flag = recommender.generateGenreSongs(username, checkedGenres)
    
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
    titles, artists, images, checked = db.sendGenreSongs(username)

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
    db.updateCheckedGenreSongs(username, checkedGenreSongs)
    #generate the playlist in the db 
    flag = recommender.generatePlaylistSongs(username, checkedGenreSongs)
    while (not flag):
        flag = recommender.generatePlaylistSongs(username, checkedGenreSongs)
    
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
    
    titles, artists, images = db.getPlaylist(username)
    
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
    titles, artists, images = db.getBacklog(username)

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
    