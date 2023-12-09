import openai
import requests
import db

openai.api_key = "" #paste in your own api key from this link https://platform.openai.com/api-keys
secretKey = '884fe27b952884ad8464bedef92a03bd' #paste your own deezer api key https://developers.deezer.com/myapps/
baseURL = 'https://api.deezer.com/search' #deezer track search 

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
    images.append(getCoverArt(fields[0], fields[1]))
  
  #create db connection  
  connection = db.connectDB().connection
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
    images.append(getCoverArt(fields[0], fields[1]))
  
  connection = db.connectDB().connection
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

#get the cover art of a song given a title and artist
def getCoverArt(title, artist):
  #format parameters to send to deezer for search
  params = {
        'q': f'{title} {artist}',
    }

  #format headers to send to deezer for search
  headers = {
        'Accept': 'application/json',
        'Content-Type': 'application/json',
        'User-Agent': 'YourApp/1.0.0',  
    }

  #send a request to deezer to get formation for the track
  response = requests.get(baseURL, params=params, headers=headers)
  data = response.json()

  if 'data' in data and data['data']:
      cover_art_url = data['data'][0]['album']['cover_big']  
      #print(cover_art_url)
      return cover_art_url
  else:
      #will return False if coverart is not available 
      return False
  


  
 
 
  
  
  
  

    
  
  
  
  

  


  
