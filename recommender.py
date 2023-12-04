import openai
import requests
from flask import jsonify
import recommender

openai.api_key = "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" #paste in your own api key from this link https://platform.openai.com/api-keys
secretKey = '884fe27b952884ad8464bedef92a03bd' #paste your own deezer api key https://developers.deezer.com/myapps/
baseURL = 'https://api.deezer.com/search' #sending get reqeusts to this website

def songListGeneration(genresList): ###IF CONTAINS \N, more than 2 ",or error RERUN THE FUNCTION
  response = openai.chat.completions.create(
    model="gpt-3.5-turbo",
    messages=[
      {"role": "system", "content": "You are a song recommender that will recommend 10 songs when given genres. OUTPUT THE RESULT IN THE FORM OF A PYTHON ARRAY ON ONE LINE. FOLLOW THE FORMAT 'song - artist' for every song"},
      {"role": "user", "content": "return this array ['song1 - artist1', 'song2 - artist2', 'song3 - artist3', 'song4 - artist4', 'song5 - artist5', 'song6 - artist6', 'song7 - artist7', 'song8 - artist8', 'song9 - artist9', 'song10 - artist10'] but populate each songs and artists with real songs and artists from genres: {}".format(genresList)}
    ])
  songsFromGenres = response.choices[0].message.content[2:-2].split("', '")
  print(songsFromGenres)
  
  titles = []
  artists = []
  images =[]
  
  for song in songsFromGenres:
    fields = song.split(" - ")
    titles.append(fields[0])
    artists.append(fields[1])
    images.append(getCoverArt(fields[0], fields[1]))
  
  return titles, artists, images
  return jsonify({
              'songs': titles,
              'artists': artists,
              'images': images,
              'message': 'should be 10 from index 0-9'
            })  

  
def recommendMusic(userSongs):
  response = openai.chat.completions.create(
    model="gpt-3.5-turbo",
    messages=[
      {"role": "system", "content": "You are a song recommender that will recommend 5 similar songs when given songs. OUTPUT THE RESULT IN THE FORM OF A PYTHON ARRAY ON ONE LINE. FOLLOW THE FORMAT 'song - artist' for every song"},
      {"role": "user", "content": "return this array ['song1 - artist1', 'song2 - artist2', 'song3 - artist3', 'song4 - artist4', 'song5 - artist5'] but populate each songs and artists with similar songs and artist to: {}".format(userSongs)} 
    ])
  playlist = response.choices[0].message.content[2:-2].split("', '")
  print(playlist)

  titles = []
  artists = []
  images =[]

  for song in playlist:
    fields = song.split(" - ")
    titles.append(fields[0])
    artists.append(fields[1])
    images.append(getCoverArt(fields[0], fields[1]))
    
  return titles, artists, images
  return jsonify({
              'songs': titles,
              'artists': artists,
              'images': images,
              'message': 'should be 5 from index 0-4'
            })

def getCoverArt(song, artist):
  params = {
        'q': f'{song} {artist}',
    }

  headers = { #leave like this is fine
        'Accept': 'application/json',
        'Content-Type': 'application/json',
        'User-Agent': 'YourApp/1.0.0',  
    }

  response = requests.get(baseURL, params=params, headers=headers)
  data = response.json()

  if 'data' in data and data['data']:
      cover_art_url = data['data'][0]['album']['cover_big']  
      #print(cover_art_url)
      return cover_art_url
  else:
      #print(f"No cover art available for {song} by {artist} on Deezer.")
      return False
  

if __name__=='__main__': #for testing
  
  userSongs = ['A lot - 21 Savage', 'omomo punk - warrenhue', 'Prom - SZA'] 
  genresList = ['R&B']
  
  titles, artists, images = recommendMusic(userSongs)
  for i in range(5):
    print(titles[i])
    print(artists[i])
    print(images[i])
    print()

  print('----------------------------------------------------------')
  
  titles, artists, images = songListGeneration(genresList)
  for i in range(10):
    print(titles[i])
    print(artists[i])
    print(images[i])
    print()
    
  
 
 
  
  
  
  

    
  
  
  
  

  


  
