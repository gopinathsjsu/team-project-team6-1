
from connection import connection
import psycopg2
import psycopg2.extras
import datetime
from flask import jsonify
import json


conn = None
# read connection parameters
params = connection()
 

'''

class CursorByName():
    def __init__(self, cursor):
        self._cursor = cursor
    
    def __iter__(self):
        return self

    def __next__(self):
        row = self._cursor.__next__()
        return { description[0]: row[col] for col, description in enumerate(self._cursor.description) }

'''

#checks username and password for login; returns username and membership details
def checkLoginCredentials(username, password):
    
    data = []
    try:
        #establish connection
        with psycopg2.connect(**params) as conn:

            # create a cursor 
            with conn.cursor(cursor_factory = psycopg2.extras.RealDictCursor) as cur:

                #write query
                query = f'''SELECT username, membership.* FROM usertable
                        INNER JOIN (
                            SELECT * from usermembership
                        )membership
                        on usertable.userid = membership.userid
                        WHERE username = %s AND userpassword = %s'''
                        
                #fetch data from server
                cur.execute(query, (username, password))

                '''
                for row in CursorByName(cur):
                    data.append(row)
                '''

                data = cur.fetchall()
                #print(data)
                #print('successfully read in data')
                if len(data) ==0:
                    data.append({"error":"No record found"})
                    data.append({"error details": "No record found with username and password"})
    except (Exception, psycopg2.DatabaseError) as error:
        #print("Error in checkLoginCredentials()")
        #print(error)
        data.append({"error":"Error in checkLoginCredentials()"})
        data.append({"error details": str(error)})
    finally:
        if conn is not None:
            conn.close()
            print('database connection closed')
            return data
        
#returns list of currently showing movies
def getCurrentMovies():
    data = []
    try:
        with psycopg2.connect(**params) as conn:

            with conn.cursor(cursor_factory = psycopg2.extras.RealDictCursor) as cur:

                query = f'''SELECT movieid, moviename, runtimeminutes, poster
	                    FROM movie WHERE releasedate < CURRENT_DATE AND endshowingdate > CURRENT_DATE'''
                
                cur.execute(query)

                data = cur.fetchall()
                if len(data) ==0:
                    data.append({"error":"No record found"})
                    data.append({"error details": "No movies showing currently!"})
    except (Exception, psycopg2.DatabaseError) as error:
        data.append({"error":"Error in getCurrentMovies()"})
        data.append({"error details": str(error)})
    finally:
        if conn is not None:
            conn.close()
            return data

#returns list of upcoming movies
def getUpcomingMovies():
    data = []
    try:
        with psycopg2.connect(**params) as conn:

            with conn.cursor(cursor_factory = psycopg2.extras.RealDictCursor) as cur:

                query = f'''SELECT movieid, moviename, runtimeminutes, poster
	                    FROM movie WHERE releasedate > CURRENT_DATE'''
                
                cur.execute(query)

                data = cur.fetchall()
                if len(data) ==0:
                    data.append({"error":"No record found"})
                    data.append({"error details": "No upcoming movies!"})
    except (Exception, psycopg2.DatabaseError) as error:
        data.append({"error":"Error in getUpcomingMovies()"})
        data.append({"error details": str(error)})
    finally:
        if conn is not None:
            conn.close()
            return data

#returns list of all multiplexes
def getMultiplexList():
    data = []
    try:
        with psycopg2.connect(**params) as conn:

            with conn.cursor(cursor_factory = psycopg2.extras.RealDictCursor) as cur:

                query = f'''SELECT multiplexid, multiplexname FROM multiplex'''
                
                cur.execute(query)

                data = cur.fetchall()
                if len(data) ==0:
                    data.append({"error":"No record found"})
                    data.append({"error details": "No multiplexes found!"})
    except (Exception, psycopg2.DatabaseError) as error:
        data.append({"error":"Error in getMultiplexList()"})
        data.append({"error details": str(error)})
    finally:
        if conn is not None:
            conn.close()
            return data

#retuns all the multiplexes, theater and date information for the given movie
def getShowingInfo(movieid, multiplexid, date):
    data = []
    try:
        with psycopg2.connect(**params) as conn:

            with conn.cursor(cursor_factory = psycopg2.extras.RealDictCursor) as cur:
                query = f'''SELECT * FROM showingmaster
                            INNER JOIN(
                                SELECT theaterid, theater.multiplexid, theaternumber, multiplexname  from theater
                                    INNER JOIN (
                                        SELECT multiplexname, multiplex.multiplexid from multiplex where multiplex.multiplexid = %s
                                    )mul1
                                    on theater.multiplexid = mul1.multiplexid
                                )t1
                            ON showingmaster.theaterid = t1.theaterid
                            INNER JOIN(
                                SELECT movieid, moviename, poster from movie where movieid = %s
                                GROUP BY movieid
                                )m1
                            ON showingmaster.movieid = m1.movieid
                            INNER JOIN (
                                SELECT showingdetails.showingid, STRING_AGG(showtime::text, ', ' ORDER BY showtime) AS mshowtimes,
                                STRING_AGG(showingdetails.showingid::text, ', ' ORDER BY showingdetails.showingid) AS showingids,
                                STRING_AGG(discount::text, ', ' ORDER BY discount) AS discounts
                                FROM showingdetails WHERE showdate = %s AND seatsavailable >0 
                                GROUP BY showingdetails.showingid
                                )sd
                            ON showingmaster.showingid = sd.showingid;'''
                cur.execute(query, (multiplexid, movieid, date))

                data = cur.fetchall()
                if len(data) ==0:
                    data.append({"error":"No record found"})
                    data.append({"error details": "No theaters for the selected movie and date!"})
    except (Exception, psycopg2.DatabaseError) as error:
        data.append({"error":"Error in getShowingInfo()"})
        data.append({"error details": str(error)})
    finally:
        if conn is not None:
            conn.close()
            data = json.dumps(data, indent=4, sort_keys=True, default=str) # to deal with date not being JSON serializable
            data = json.loads(data)
            return data

#returns all the seats from seatdetail table for a showing detail
def getseatAllocation(theaterid, showdetailid):
    data = []
    try:
        with psycopg2.connect(**params) as conn:

            with conn.cursor(cursor_factory = psycopg2.extras.RealDictCursor) as cur:
                query = f'''SELECT * FROM seatdetails
                            INNER JOIN (
                                SELECT seatid,rownum,seatno FROM seat WHERE theaterid = %s
                            )st
                            ON seatdetails.seatid = st.seatid
                            WHERE showingdetailid =%s;'''
                cur.execute(query, (theaterid, showdetailid))

                data = cur.fetchall()
                if len(data) ==0:
                    data.append({"error":"No record found"})
                    data.append({"error details": "No seatdeatils records for the selected movie, theater and date!"})
    except (Exception, psycopg2.DatabaseError) as error:
        data.append({"error":"Error in getseatAllocation()"})
        data.append({"error details": str(error)})
    finally:
        if conn is not None:
            conn.close()
            return data

#creates temperory booking number
def createBooking(seatid, showingdetailid,userid):
    data = []
    try:
        with psycopg2.connect(**params) as conn:

            with conn.cursor(cursor_factory = psycopg2.extras.RealDictCursor) as cur:
                query = f'''INSERT INTO booking(num_seats_booked, seatid, showingdetailid, userid) VALUES (%s, %s, %s,%s) RETURNING bookingid;'''
                cur.execute(query, (len(seatid), seatid, showingdetailid, userid))

                data = cur.fetchall()
                if len(data) ==0:
                    data.append({"error":"Record not created"})
                    data.append({"error details": "Booking record not created"})
    except (Exception, psycopg2.DatabaseError) as error:
        data.append({"error":"Error in createBooking()"})
        data.append({"error details": str(error)})
    finally:
        if conn is not None:
            conn.close()
            return data

def completeBooking(bookingid, payment, rewardpointsused, seats):
    data = []
    try:
        with psycopg2.connect(**params) as conn:

            with conn.cursor(cursor_factory = psycopg2.extras.RealDictCursor) as cur:
                print("{" + (",".join(map(str, seats))) + "}")
                query = f'''SELECT seatdetailid FROM seatdetails WHERE seatdetailid = ANY (%s::int[]) and istaken = TRUE;'''
                cur.execute(query, ("{" + (",".join(map(str, seats))) + "}",))
                data = cur.fetchall()
                if len(data) > 0:
                    data.append({"error":"Seat cannot be be assigned"})
                    data.append({"error details": "Seats already taken"})
                    return data

                query = f'''UPDATE seatdetails set istaken = true WHERE seatdetailid = ANY (%s::int[]) and istaken = false RETURNING seatdetailid;'''
                cur.execute(query, ("{" + (",".join(map(str, seats))) + "}",))
                data = cur.fetchall()
                if len(data) < len(seats):
                    data.append({"error":"Seat cannot be be assigned"})
                    data.append({"error details": "Seats already taken"})
                    return data


                query = f'''UPDATE booking set status = %s, totalcost = %s, discount = %s, servicefee = %s, 
                            rewardpointsused = %s, rewardpointsearned = %s
	                        WHERE bookingid = %s RETURNING bookingid;'''
                cur.execute(query, ('true',payment['total']-rewardpointsused, payment['discount'], payment['fee'], rewardpointsused, payment['total']-rewardpointsused, bookingid))

                data = cur.fetchall()
                if len(data) ==0:
                    data.append({"error":"Record not created"})
                    data.append({"error details": "Booking record not created"})
    except (Exception, psycopg2.DatabaseError) as error:
        data.append({"error":"Error in createBooking()"})
        data.append({"error details": str(error)})
    finally:
        if conn is not None:
            conn.close()
            return data


#get card details
def getCardDetails(userid):
    data = []
    try:
        with psycopg2.connect(**params) as conn:

            with conn.cursor(cursor_factory = psycopg2.extras.RealDictCursor) as cur:
                query = f'''SELECT cardid FROM CardDetails WHERE userid = %s;'''
                cur.execute(query, (userid,))

                data = cur.fetchall()
                if len(data) ==0:
                    data.append({"error":"Record not found"})
                    data.append({"error details": "Card record not found for the user"})
    except (Exception, psycopg2.DatabaseError) as error:
        data.append({"error":"Error in getCardDetails()"})
        data.append({"error details": str(error)})
    finally:
        if conn is not None:
            conn.close()
            return data

#get booking details
def getTransactionDetails(bookingid):
    data = []
    try:
        with psycopg2.connect(**params) as conn:

            with conn.cursor(cursor_factory = psycopg2.extras.RealDictCursor) as cur:
                query = f'''SELECT booking.showingdetailid, ARRAY_LENGTH(seatid,1), seatid, sd.* FROM booking
                            INNER JOIN(
                            SELECT showingdetails.showingid, showingdetails.showingdetailid, showdate, showtime, discount, sm.* FROM showingdetails
                                INNER JOIN(
                                SELECT price, showingmaster.showingid FROM showingmaster
                                )sm
                                ON sm.showingid = showingdetails.showingid
                            )sd
                            ON sd.showingdetailid = booking.showingdetailid
                            WHERE bookingid =%s;'''
                cur.execute(query, (bookingid,))

                data = cur.fetchall()
                if len(data) ==0:
                    data.append({"error":"Record not found"})
                    data.append({"error details": "Booking record not found"})
    except (Exception, psycopg2.DatabaseError) as error:
        data.append({"error":"Error in getTransactionDetails()"})
        data.append({"error details": str(error)})
    finally:
        if conn is not None:
            conn.close()
            data = json.dumps(data, indent=4, sort_keys=True, default=str) # to deal with date not being JSON serializable
            data = json.loads(data)
            return data

#save card details to db
def saveCardDetails(card_number, cvv,exp, userid):
    data = []
    try:
        with psycopg2.connect(**params) as conn:

            with conn.cursor(cursor_factory = psycopg2.extras.RealDictCursor) as cur:
                query = f'''UPDATE carddetails SET cardid = %s, cvv = %s, expiry = %s WHERE userid=%s;
                            INSERT INTO carddetails (cardid, cvv, expiry, userid)
                                SELECT %s, %s, %s, %s
                                WHERE NOT EXISTS (SELECT 1 FROM carddetails WHERE userid=%s);'''
                cur.execute(query, (card_number,cvv,exp,userid,card_number,cvv,exp,userid,userid))
    except (Exception, psycopg2.DatabaseError) as error:
        data.append({"error":"Error in saveCardDetails()"})
        data.append({"error details": str(error)})
    finally:
        if conn is not None:
            conn.close()
            return data

# to register a user 
def registeruser(fullname, phoneno, address, username, password, role):
    data = {}  # Use a dictionary to store the response data
    try:
        # Establish connection and create a cursor
        with psycopg2.connect(**params) as conn:
            # Create a cursor
            cur = conn.cursor()

            # Write query
            query = '''INSERT INTO usertable (userid,fullname, phonenumber, address, username, userpassword, userrole) VALUES (%s, %s, %s, %s, %s, %s, %s);'''
            cur.execute('''select max(userid) from usertable;''')
            max_id = cur.fetchone()[0]
            print(max_id)
            if (max_id != None):
            # Execute the query
                cur.execute(query, (max_id+1,fullname, phoneno, address, username, password, role))
            else:
                cur.execute(query, (1,fullname, phoneno, address, username, password, role))
                
            conn.commit()

            # Set success response data
            data['success'] = True
            data['message'] = 'User registration successful'

    except (Exception, psycopg2.DatabaseError) as error:
        print("Error in registeruser()")
        print(error)
        data['success'] = False
        data['error'] = 'Error in user registration'
        data['error_details'] = str(error)
    return jsonify(data)

# to register user as having Regular membership as soon as they register
def registerUserMembership(username):
    #global conn
    print("I am in registerUserMmebership")
    data = []
    try:
        #establish connection
        with psycopg2.connect(**params) as conn:

            # create a cursor 
                cursor = conn.cursor()
                print("hello world")
                query = '''INSERT INTO usermembership (membershipid, rewardpoints, ispremium, membershiptilldate, userid, membershiptype) VALUES (%s, %s, %s, %s, %s, %s);'''
                cursor.execute('''select max(membershipid) from usermembership;''')
                max_id = cursor.fetchone()[0]
                if (max_id == None):
                    max_id = 0
                print(max_id)
                query2 = "SELECT userid FROM usertable WHERE username = %s;"
                cursor.execute(query2,(username,))
                userid = cursor.fetchone()[0]
                print("User id :",userid)
                curDate = datetime.date.today()
                newYear = curDate.year+1
                insertDate = curDate.replace(year=newYear).strftime('%Y-%m-%d')
                print(insertDate)
                
                cursor.execute(query, (max_id + 1, 0, 'false', insertDate, userid, "Regular"))
                conn.commit()
                cursor = conn.cursor(cursor_factory = psycopg2.extras.RealDictCursor)
                query3 = "select * from usermembership where membershipid=%s"
                cursor.execute(query3,(max_id+1,))
                data = cursor.fetchone()
                print(data)
                if len(data) ==0:
                    data.append({"error":"No record found"})
                    data.append({"error details": "No record found with membershipid"})
    except (Exception, psycopg2.DatabaseError) as error:
        data.append({"error":"Error in inserting usermembership"})
        data.append({"error details": str(error)})
    finally:
        if conn is not None:
            conn.close()
            print('database connection closed')
        data = json.dumps(data, indent=4, sort_keys=True, default=str) # to deal with date not being JSON serializable
        data = json.loads(data)
        return data
        
# function to upgrade user's membership to Premium
def upgradeMembership(username):
    data = []
    try:
        #establish connection
        with psycopg2.connect(**params) as conn:

            # create a cursor 
                cursor = conn.cursor()
                preQuery = "SELECT userid FROM usertable WHERE username = %s;"
                cursor.execute(preQuery,(username,))
                userid = cursor.fetchone()[0]
                query = "UPDATE usermembership SET membershiptype = %s, ispremium = %s WHERE userid = %s;"
                cursor.execute(query,('Premium','true',userid,))
                conn.commit()
                cursor = conn.cursor(cursor_factory = psycopg2.extras.RealDictCursor)
                confirmSuccessQuery = "select * from usermembership where userid=%s"
                cursor.execute(confirmSuccessQuery,(userid,))
                data = cursor.fetchone()
                print(data)
                if len(data) ==0:
                    data.append({"error":"No record found"})
                    data.append({"error details": "No record found with userid"})
    except (Exception, psycopg2.DatabaseError) as error:
        data.append({"error":"Error in upgrading user membership to premium"})
        data.append({"error details": str(error)})
    finally:
        if conn is not None:
            conn.close()
            print('database connection closed')
        return jsonify(data)
    

# function to get user's profile info
def getProfileInfo(username):
    data = []
    try:
        #establish connection
        with psycopg2.connect(**params) as conn:

            # create a cursor 
                cursor = conn.cursor(cursor_factory = psycopg2.extras.RealDictCursor)
                query = "select fullname, address, membershiptype, membershiptilldate, rewardpoints from usertable inner join usermembership on usertable.userid = usermembership.userid where username=%s;"
                cursor.execute(query,(username,))
                data = cursor.fetchone()
                print(data)
                if len(data) ==0:
                    data.append({"error":"No record found"})
                    data.append({"error details": "No record found for this username"})
    except (Exception, psycopg2.DatabaseError) as error:
        data.append({"error":"Error in retrieving profile info"})
        data.append({"error details": str(error)})
    finally:
        if conn is not None:
            conn.close()
            print('database connection closed')
        data = json.dumps(data, indent=4, sort_keys=True, default=str) # to deal with date not being JSON serializable
        data = json.loads(data)
        return jsonify(data)
    

# function to get user's past movie bookings to display on profile section
def getPastMovieBookings(username):
    data = []
    try:
        #establish connection
        with psycopg2.connect(**params) as conn:

            # create a cursor 
                cursor = conn.cursor()
                preQuery = "SELECT userid FROM usertable WHERE username = %s;"
                cursor.execute(preQuery,(username,))
                userid = cursor.fetchone()[0]
                cursor = conn.cursor(cursor_factory = psycopg2.extras.RealDictCursor)
                # query = "select bookingid, num_seats_booked,totalcost,servicefee,showdate,showtime,price,moviename,runtimeminutes from (select * from (select * from booking inner join showingdetails on booking.showingdetailid = showingdetails.showingdetailid where userid = %s and showingdetails.showdate < CURRENT_DATE) inner join showingmaster using (showingid)) inner join movie using (movieid);"
                query="SELECT bookingid, num_seats_booked, totalcost, servicefee, showdate, showtime, price, moviename, poster,runtimeminutes FROM (SELECT * FROM (SELECT * FROM booking INNER JOIN showingdetails ON booking.showingdetailid = showingdetails.showingdetailid WHERE userid = %s AND showingdetails.showdate < CURRENT_DATE) AS subquery1 INNER JOIN showingmaster USING (showingid)) AS subquery2 INNER JOIN movie USING (movieid);"
                cursor.execute(query,(userid,))
                data = cursor.fetchall()
                print(data)
                if len(data) ==0:
                    data.append({"error":"No record found"})
                    data.append({"error details": "No past movie info found for this username"})
    except (Exception, psycopg2.DatabaseError) as error:
        data.append({"error":"Error in retrieving user's past movie bookings"})
        data.append({"error details": str(error)})
    finally:
        if conn is not None:
            conn.close()
            print('database connection closed')
        data = json.dumps(data, indent=4, sort_keys=True, default=str) # to deal with date not being JSON serializable
        data = json.loads(data)
        return jsonify(data)
    

# function to get user's upcoming movie bookings to display on profile section
def getUpcomingMovieBookings(username):
    data = []
    try:
        #establish connection
        with psycopg2.connect(**params) as conn:

            # create a cursor 
                cursor = conn.cursor()
                preQuery = "SELECT userid FROM usertable WHERE username = %s;"
                cursor.execute(preQuery,(username,))
                userid = cursor.fetchone()[0]
                cursor = conn.cursor(cursor_factory = psycopg2.extras.RealDictCursor)
                # query = "select bookingid, num_seats_booked,totalcost,servicefee,showdate,showtime,price,moviename,runtimeminutes from (select * from (select * from booking inner join showingdetails on booking.showingdetailid = showingdetails.showingdetailid where userid = %s and showingdetails.showdate > CURRENT_DATE) inner join showingmaster using (showingid)) inner join movie using (movieid);"
                query="SELECT bookingid, num_seats_booked, totalcost, servicefee, showdate, showtime, price, moviename, poster,runtimeminutes FROM (SELECT * FROM (SELECT * FROM booking INNER JOIN showingdetails ON booking.showingdetailid = showingdetails.showingdetailid  WHERE userid = %s AND showingdetails.showdate > CURRENT_DATE) AS subquery1 INNER JOIN showingmaster USING (showingid)) AS subquery2 INNER JOIN movie USING (movieid);"
                cursor.execute(query,(userid,))
                data = cursor.fetchall()
                print(data)
                if len(data) ==0:
                    data.append({"error":"No record found"})
                    data.append({"error details": "No upcoming movie info found for this username"})
    except (Exception, psycopg2.DatabaseError) as error:
        data.append({"error":"Error in retrieving user's upcoming movie bookings"})
        data.append({"error details": str(error)})
    finally:
        if conn is not None:
            conn.close()
            print('database connection closed')
        data = json.dumps(data, indent=4, sort_keys=True, default=str) # to deal with date not being JSON serializable
        data = json.loads(data)
        return jsonify(data)
    

# function to get user's movies watched in the past 30 days
def getMoviesPast30Days(username):
    data = []
    try:
        #establish connection
        with psycopg2.connect(**params) as conn:

            # create a cursor 
                cursor = conn.cursor()
                preQuery = "SELECT userid FROM usertable WHERE username = %s;"
                cursor.execute(preQuery,(username,))
                userid = cursor.fetchone()[0]
                cursor = conn.cursor(cursor_factory = psycopg2.extras.RealDictCursor)
                # query = "select moviename from (select * from (select * from booking inner join showingdetails on booking.showingdetailid = showingdetails.showingdetailid where userid = %s and showingdetails.showdate < CURRENT_DATE) inner join showingmaster using (showingid)) inner join movie using (movieid) where showdate >= CURRENT_DATE - 30;"
                query="SELECT distinct moviename,poster FROM (SELECT * FROM (SELECT * FROM booking INNER JOIN showingdetails ON booking.showingdetailid = showingdetails.showingdetailid WHERE userid = %s AND showingdetails.showdate < CURRENT_DATE) AS subquery1 INNER JOIN showingmaster USING (showingid)) AS subquery2 INNER JOIN movie USING (movieid) WHERE showdate >= CURRENT_DATE - 30;"
                cursor.execute(query,(userid,))
                data = cursor.fetchall()
                print(data)
                if len(data) ==0:
                    data.append({"error":"No record found"})
                    data.append({"error details": "No 30 days movie history found for this username"})
    except (Exception, psycopg2.DatabaseError) as error:
        data.append({"error":"Error in retrieving user's 30 days movie history"})
        data.append({"error details": str(error)})
    finally:
        if conn is not None:
            conn.close()
            print('database connection closed')
        return jsonify(data)
    


# function to cancel user's movie booking
def cancelBooking(bookingId):
    data = []
    try:
        #establish connection
        with psycopg2.connect(**params) as conn:

            # create a cursor 
                cursor = conn.cursor()
                query = "delete FROM booking WHERE bookingid = %s;"
                cursor.execute(query,(bookingId,))
                cursor = conn.cursor(cursor_factory = psycopg2.extras.RealDictCursor)
                queryValidate = "select * from booking where bookingid = %s;"
                cursor.execute(queryValidate,(bookingId,))
                data = cursor.fetchall()
                print(data)
                if len(data) !=0:
                    data.append({"error":"Record found"})
                    data.append({"error details": "Booking could not be deleted."})
    except (Exception, psycopg2.DatabaseError) as error:
        data.append({"error":"Error in deleting movie booking"})
        data.append({"error details": str(error)})
    finally:
        if conn is not None:
            conn.close()
            print('database connection closed')
        data = json.dumps(data, indent=4, sort_keys=True, default=str) # to deal with date not being JSON serializable
        data = json.loads(data)
        return jsonify(data)
    


# function to get all multiplexes from a particular location
def getMultiplexesByLocation(locationId):
    data = []
    try:
        #establish connection
        with psycopg2.connect(**params) as conn:

            # create a cursor 
                cursor = conn.cursor(cursor_factory = psycopg2.extras.RealDictCursor)
                query = "select multiplexname FROM multiplex WHERE locationid = %s;"
                cursor.execute(query,(locationId,))
                data = cursor.fetchall()
                print(data)
                if len(data) ==0:
                    data.append({"error":"No record found"})
                    data.append({"error details": "multiplex names could not be retrieved."})
    except (Exception, psycopg2.DatabaseError) as error:
        data.append({"error":"Error in retrieving multiplex names by location"})
        data.append({"error details": str(error)})
    finally:
        if conn is not None:
            conn.close()
            print('database connection closed')
        data = json.dumps(data, indent=4, sort_keys=True, default=str) # to deal with date not being JSON serializable
        data = json.loads(data)
        return jsonify(data)
    



# function to get names of movies which have played in the past 90 days
def getMoviesPlayedPast90Days():
    data = []
    try:
        #establish connection
        with psycopg2.connect(**params) as conn:

            # create a cursor 
                cursor = conn.cursor(cursor_factory = psycopg2.extras.RealDictCursor)
                query = "SELECT DISTINCT moviename, movieid FROM (SELECT * FROM movie INNER JOIN (SELECT *FROM showingmaster INNER JOIN showingdetails ON showingmaster.showingid = showingdetails.showingid) AS subquery USING (movieid)) AS main_query WHERE showdate >= CURRENT_DATE - 90;"
                cursor.execute(query)
                data = cursor.fetchall()
                print(data)
                if len(data) ==0:
                    data.append({"error":"No record found"})
                    data.append({"error details": "No movies found which played in the past 90 days"})
    except (Exception, psycopg2.DatabaseError) as error:
        data.append({"error":"Error in retrieving movies which have played in the past 90 days."})
        data.append({"error details": str(error)})
    finally:
        if conn is not None:
            conn.close()
            print('database connection closed')
        data = json.dumps(data, indent=4, sort_keys=True, default=str) # to deal with date not being JSON serializable
        data = json.loads(data)
        return jsonify(data)
    


# function to get all cities in db
def getAllCities():
    data = []
    try:
        #establish connection
        with psycopg2.connect(**params) as conn:

            # create a cursor 
                cursor = conn.cursor(cursor_factory = psycopg2.extras.RealDictCursor)
                query = "select distinct city from location;"
                cursor.execute(query)
                data = cursor.fetchall()
                print(data)
                if len(data) ==0:
                    data.append({"error":"No record found"})
                    data.append({"error details": "No cities found in db"})
    except (Exception, psycopg2.DatabaseError) as error:
        data.append({"error":"Error in retrieving all cities in db"})
        data.append({"error details": str(error)})
    finally:
        if conn is not None:
            conn.close()
            print('database connection closed')
        data = json.dumps(data, indent=4, sort_keys=True, default=str) # to deal with date not being JSON serializable
        data = json.loads(data)
        return jsonify(data)