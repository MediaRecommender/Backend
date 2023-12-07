import db

class User:
  
    def __init__(self, username, name, password):
        self.username = username      
        self.name = name                    
        self.password = password           
    
    def insertUser(self):
        #intialize all the genres of the user to input into db
        userGenres = ['Pop', 'Rock', 'Jazz', 'Hip-Hop', 'Indie', 'EDM', 'Country', 'Classical', 'R&B', 'Metal']
            
        #connect to db
        connection = db.connectDB().connection
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

            