import db

class User:
    TABLE = "user"
    def __init__(self, email, name, password):
        self.email = email      
        self.name = name                    
        self.password = password           
    
    def insertUser(self):
        try:
            #Connect to db
            connection = db.connectDB().connection
            cursor = connection.cursor()

            #query to user info into database
            query = 'INSERT INTO users(email, name, password) VALUES (%s, %s, %s);'
            vals = (self.email, self.name, self.password)
            print(vals)

            #execut the query 
            cursor.execute(query, vals)

            #coomit the connection to actually change the table in db
            connection.commit()
            #close cursor
            cursor.close()

        except Exception as e:
            print(f"Error: {str(e)}")