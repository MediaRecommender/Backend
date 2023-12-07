from flask import Flask, request, render_template, jsonify
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

@app.route('/register')
def register():
    return render_template('register.html')

#page for user to select genres they are interested in 
#sends frontend checked genres to preserve previous survey answers
@app.route('/survey', methods = ['GET', 'POST']) 
def survey():
    #access and store json package containing genres array
    data = request.get_json()
    #need username to specify which user to make songs for
    username = data['username']
    
    #create array to return list of user's checked genres in survey
    checkedGenres = []
    
    #use db function to get user's checked genres and store the query into variable 
    query = db.sendCheckedGenres(username)
    
    #append each genre into array
    for genre in query:
        checkedGenres.append(genre['genre'])
        print(genre)

    #return genre array in json package
    return jsonify({
        'checkedGenres': checkedGenres
    })

#page for the user to select songs based off genres they selected on survey page
#updates checked genres in db right after taking the survey and going to survey results page
@app.route('/surveyResults', methods=['GET', 'POST']) #CHECK IF USERNAME ENTRIES ARE IN USERGENRESONGS, IF THEY ARE SKIP THE GENRESONG FUNCTION

def surveyResults():
    #access and store json package containing genres array
    data = request.get_json()
    #need username to specify which user to make songs for
    username = data['username']
    #get list of genres user checked 
    checkedGenres = data['checkedGenres']
    
    #return false if user did not check any genres, hence array will be empty
    if not checkedGenres:
        return jsonify({
            'success':False
        })
        
    #update user's checked genres in db
    db.updateCheckedGenres(username, checkedGenres)
    
    #save returned arrays from genreSongs function
    titles, artists, images = recommender.genreSongs(username, checkedGenres)
    
    #return 10 songs in json package
    return jsonify({
        'title0': titles[0],
        'artist0': artists[0],
        'image0': images[0],
        'title1': titles[1],
        'artist1': artists[1],
        'image1': images[1],
        'title2': titles[2],
        'artist2': artists[2],
        'image2': images[2],
        'title3': titles[3],
        'artist3': artists[3],
        'image3': images[3],
        'title4': titles[4],
        'artist4': artists[4],
        'image4': images[4],
        'title5': titles[5],
        'artist5': artists[5],
        'image5': images[5],
        'title6': titles[6],
        'artist6': artists[6],
        'image6': images[6],
        'title7': titles[7],
        'artist7': artists[7],
        'image7': images[7],
        'title8': titles[8],
        'artist8': artists[8],
        'image8': images[8],
        'title9': titles[9],
        'artist9': artists[9],
        'image9': images[9],
        })

    
#user's final playlist page    
@app.route('/playlistResults', methods=['GET', 'POST']) 
def playlistResults():
    #access and store json package containing array of user selected songs from genresSongs
    data = request.get_json()
    #need username to specify which user to make songs for
    username = data['username']
    #get list of songs user checked 
    checkedSongs = data['checkedSongs']
    
    #return false if user did not check any songs, hence array will be empty
    if not checkedSongs:
        return jsonify({
            'success': False
        })
        
    #update user's checked songs in db
    db.updateCheckedSongs(username, checkedSongs) #CHECKED SONGS END UP BEING "TITLE - ARTIST" ONLY WORKS WITH "TITLE"
    
    #save returned arrays from genreSongs function
    titles, artists, images = recommender.recommendMusic(username, checkedSongs)
    
    #return 10 final songs in json package
    return jsonify({
        'title0': titles[0],
        'artist0': artists[0],
        'image0': images[0],
        'title1': titles[1],
        'artist1': artists[1],
        'image1': images[1],
        'title2': titles[2],
        'artist2': artists[2],
        'image2': images[2],
        'title3': titles[3],
        'artist3': artists[3],
        'image3': images[3],
        'title4': titles[4],
        'artist4': artists[4],
        'image4': images[4],
        'title5': titles[5],
        'artist5': artists[5],
        'image5': images[5],
        'title6': titles[6],
        'artist6': artists[6],
        'image6': images[6],
        'title7': titles[7],
        'artist7': artists[7],
        'image7': images[7],
        'title8': titles[8],
        'artist8': artists[8],
        'image8': images[8],
        'title9': titles[9],
        'artist9': artists[9],
        'image9': images[9],
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

if __name__=='__main__':
    app.run(debug=True)
    