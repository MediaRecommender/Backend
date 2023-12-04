import db
from app import app

class Song:
   
    def __init__(self, title, artist, imageURL):
        self.title = title      
        self.artist = artist                    
        self.imageURL = imageURL 
        
    def insertSong(self):
        try:
            #Connect to db
            connection = db.connectDB().connection
            cursor = connection.cursor()

            #query to user info into database
            query = 'INSERT INTO songs(title, artist, imageURL) VALUES (%s, %s, %s);'
            vals = (self.title, self.artist, self.imageURL)
            print(vals)

            #execut the query 
            cursor.execute(query, vals)

            #coomit the connection to actually change the table in db
            connection.commit()
            #close cursor
            cursor.close()

        except Exception as e:
            print(f"Error: {str(e)}")
