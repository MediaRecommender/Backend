import openai
import requests

openai.api_key = "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" #paste in your own api key from this link https://platform.openai.com/api-keys
secretKey = '884fe27b952884ad8464bedef92a03bd' #paste your own deezer api key https://developers.deezer.com/myapps/
baseURL = 'https://api.deezer.com/search' #deezer track search 

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
  