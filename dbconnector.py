
from connection import connection
import psycopg2

conn = None
# read connection parameters
params = connection()

class CursorByName():
    def __init__(self, cursor):
        self._cursor = cursor
    
    def __iter__(self):
        return self

    def __next__(self):
        row = self._cursor.__next__()
        return { description[0]: row[col] for col, description in enumerate(self._cursor.description) }
    

def checkLoginCredentials(requestdata):
    username = requestdata["username"]
    password = requestdata["password"]
    print(username)
    print(password)
    data = []
    try:
        #establish connection
        with psycopg2.connect(**params) as conn:

            # create a cursor 
            with conn.cursor() as cur:

                #write query
                query = f'SELECT username FROM usertable WHERE username = %s AND userpassword = %s'
                #query = f'SELECT * FROM usertable'

                #fetch data from server
                cur.execute(query, (username, password)) 

                for row in CursorByName(cur):
                    data.append(row)

                #data = cur.fetchall()
                print(data)
                print('successfully read in data')
    except (Exception, psycopg2.DatabaseError) as error:
        print("Error in checkLoginCredentials()")
        print(error)
        data.append({"error":"Error in checkLoginCredentials()"})
        data.append({"error details": str(error)})
    finally:
        if conn is not None:
            conn.close()
            print('database connection closed')
            return data