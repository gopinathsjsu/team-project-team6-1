
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
                                SELECT * FROM seat
                                INNER JOIN (
                                    SELECT noofrows, noofcolumns, theater.theaterid FROM theater
                                )th
                                ON seat.theaterid = th.theaterid
                                WHERE seat.theaterid = %s
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

#add all the booking info after payment is successful
def completeBooking(bookingid, payment, rewardpointsused, seats):
    data = []
    try:
        with psycopg2.connect(**params) as conn:

            with conn.cursor(cursor_factory = psycopg2.extras.RealDictCursor) as cur:
                query = f'''SELECT seatdetailid FROM seatdetails WHERE seatdetailid = ANY (%s::int[]) and istaken = TRUE;'''
                cur.execute(query, ("{" + (",".join(map(str, seats))) + "}",))
                data = cur.fetchall()
                if len(data) > 0:
                    data.append({"error":"Seat cannot be be assigned"})
                    data.append({"error details": "Seats already taken"})
                    return data

                query = f'''UPDATE seatdetails set istaken = true WHERE seatdetailid = ANY (%s::int[]) and istaken = false RETURNING seatdetailid;'''
                cur.execute(query, ("{" + (",".join(map(str, seats))) + "}",))
                
                data1 = cur.fetchall()
                data.append(data1[0])
                
                if len(data) < len(seats):
                    data.append({"error":"Seat cannot be be assigned"})
                    data.append({"error details": "Seats already taken"})
                    return data


                query = f'''UPDATE booking set status = %s, totalcost = %s, discount = %s, servicefee = %s, 
                            rewardpointsused = %s, rewardpointsearned = %s
	                        WHERE bookingid = %s RETURNING num_seats_booked, showingdetailid, bookingid;'''
                cur.execute(query, ('true',payment['total']-rewardpointsused, payment['discount'], payment['fee'], rewardpointsused, payment['total']-rewardpointsused, bookingid))

                data1 = cur.fetchall()
                data.append(data1[0])
                if len(data) ==0:
                    data.append({"error":"Record not created"})
                    data.append({"error details": "Booking record not created"})

                num_seat =  data1[0]["num_seats_booked"]
                showdet = data1[0]["showingdetailid"]

                query = f'''SELECT seatsavailable, seatstaken FROM showingdetails
                            WHERE showingdetailid=%s;'''
                cur.execute(query, (showdet, ))

                data1 = cur.fetchall()
                data.append(data1[0])

                if len(data) ==0:
                    data.append({"error":"Record not found"})
                    data.append({"error details": "Showingdetailid record not found"})

                query = f'''UPDATE showingdetails
                            SET seatsavailable=%s, seatstaken=%s
                            WHERE showingdetailid=%s RETURNING showingdetailid;'''
                cur.execute(query, (data1[0]["seatsavailable"] -num_seat, data1[0]["seatstaken"] + num_seat, showdet))
                data1 = cur.fetchall()
                data.append(data1[0])
                
                if len(data) ==0:
                    data.append({"error":"Record not updated"})
                    data.append({"error details": "Showingdetailid record not updated"})


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

#create new movie record in db
def createMovie(name, runtimeminutes, releasedate, endshowingdate, poster):
    data = []
    try:
        with psycopg2.connect(**params) as conn:

            with conn.cursor(cursor_factory = psycopg2.extras.RealDictCursor) as cur:
                query = f'''INSERT INTO movie(moviename, runtimeminutes, releasedate, endshowingdate, poster) VALUES (%s, %s, %s,%s, %s) RETURNING movieid;'''
                cur.execute(query, (name, runtimeminutes, releasedate, endshowingdate, poster))

                data = cur.fetchall()
                if len(data) ==0:
                    data.append({"error":"Record not created"})
                    data.append({"error details": "Movie record not created"})
    except (Exception, psycopg2.DatabaseError) as error:
        data.append({"error":"Error in createMovie()"})
        data.append({"error details": str(error)})
    finally:
        if conn is not None:
            conn.close()
            return data

#create new location record in db
def createLocation(city, postalcode, noofmultiplex):
    data = []
    try:
        with psycopg2.connect(**params) as conn:

            with conn.cursor(cursor_factory = psycopg2.extras.RealDictCursor) as cur:
                query = f'''INSERT INTO location( city, postalcode, noofmultiplex) VALUES (%s, %s, %s) RETURNING locationid;'''
                cur.execute(query, (city, postalcode, noofmultiplex))

                data = cur.fetchall()
                if len(data) ==0:
                    data.append({"error":"Record not created"})
                    data.append({"error details": "Location record not created"})
    except (Exception, psycopg2.DatabaseError) as error:
        data.append({"error":"Error in createLocation()"})
        data.append({"error details": str(error)})
    finally:
        if conn is not None:
            conn.close()
            return data

#create new multiplex record in db
def createMultiplex(name, locationid, address, nooftheaters):
    data = []
    try:
        with psycopg2.connect(**params) as conn:

            with conn.cursor(cursor_factory = psycopg2.extras.RealDictCursor) as cur:
                query = f'''INSERT INTO multiplex( multiplexname, locationid, address, nooftheaters) VALUES (%s, %s, %s, %s) RETURNING multiplexid;'''
                cur.execute(query, (name, locationid, address, nooftheaters))

                data = cur.fetchall()
                if len(data) ==0:
                    data.append({"error":"Record not created"})
                    data.append({"error details": "Multiplex record not created"})
    except (Exception, psycopg2.DatabaseError) as error:
        data.append({"error":"Error in createMultiplex()"})
        data.append({"error details": str(error)})
    finally:
        if conn is not None:
            conn.close()
            return data


#create new theater record and respective seat records in seat table in db
def createTheater(multiplexid, noofseats, theaternumber, noofrows, noofcolumns):
    data = []
    try:
        with psycopg2.connect(**params) as conn:

            with conn.cursor(cursor_factory = psycopg2.extras.RealDictCursor) as cur:
                query = f'''INSERT INTO theater(multiplexid, noofseats, theaternumber, noofrows, noofcolumns) VALUES (%s, %s, %s, %s, %s) RETURNING theaterid;'''
                cur.execute(query, (multiplexid, noofseats, theaternumber, noofrows, noofcolumns))

                data = cur.fetchall()
                if len(data) ==0:
                    data.append({"error":"Record not created"})
                    data.append({"error details": "Theater record not created"})
                else:
                    query = f'''INSERT INTO seat(rownum, seatno, theaterid) VALUES (%s, %s, %s) RETURNING seatid;'''
                    print(query)
                    values = []
                    for i in range(noofrows):
                        for j in range(noofcolumns):
                            values.append(tuple((i, j, data[0]["theaterid"])))
                    cur.executemany(query,values)
                    '''
                    seatdata = cur.fetchall()
                    if len(seatdata) < noofseats:
                        data[0]["error"]="Record not created"
                        data[0]["error details"] = "Seat record not created"
                    '''
    except (Exception, psycopg2.DatabaseError) as error:
        data.append({"error":"Error in createTheater()"})
        data.append({"error details": str(error)})
    finally:
        if conn is not None:
            conn.close()
            return data

#update movie record in db
def updateMovie(movieid, runtimeminutes, endshowingdate, poster):
    data = []
    try:
        with psycopg2.connect(**params) as conn:

            with conn.cursor(cursor_factory = psycopg2.extras.RealDictCursor) as cur:
                query = f'''UPDATE movie set runtimeminutes = %s, endshowingdate =%s, poster= %s WHERE movieid =%s RETURNING movieid;'''
                cur.execute(query, ( runtimeminutes, endshowingdate, poster, movieid))

                data = cur.fetchall()
                if len(data) ==0:
                    data.append({"error":"Record not updated"})
                    data.append({"error details": "Movie record not updated"})
    except (Exception, psycopg2.DatabaseError) as error:
        data.append({"error":"Error in updateMovie()"})
        data.append({"error details": str(error)})
    finally:
        if conn is not None:
            conn.close()
            return data


#update location record in db
def updateLocation(locationid, noofmultiplex):
    data = []
    try:
        with psycopg2.connect(**params) as conn:

            with conn.cursor(cursor_factory = psycopg2.extras.RealDictCursor) as cur:
                query = f'''UPDATE location SET noofmultiplex = %s WHERE locationid = %s RETURNING locationid;'''
                cur.execute(query, (noofmultiplex,locationid))

                data = cur.fetchall()
                if len(data) ==0:
                    data.append({"error":"Record not updated"})
                    data.append({"error details": "Location record not updated"})
    except (Exception, psycopg2.DatabaseError) as error:
        data.append({"error":"Error in updateLocation()"})
        data.append({"error details": str(error)})
    finally:
        if conn is not None:
            conn.close()
            return data

#update multiplex record in db
def updateMultiplex(multiplexid, name, address, nooftheaters):
    data = []
    try:
        with psycopg2.connect(**params) as conn:

            with conn.cursor(cursor_factory = psycopg2.extras.RealDictCursor) as cur:
                query = f'''UPDATE multiplex SET multiplexname = %s, address = %s, nooftheaters =%s WHERE multiplexid = %s RETURNING multiplexid;'''
                cur.execute(query, (name, address, nooftheaters, multiplexid))

                data = cur.fetchall()
                if len(data) ==0:
                    data.append({"error":"Record not updated"})
                    data.append({"error details": "Multiplex record not updated"})
    except (Exception, psycopg2.DatabaseError) as error:
        data.append({"error":"Error in updateMultiplex()"})
        data.append({"error details": str(error)})
    finally:
        if conn is not None:
            conn.close()
            return data

#update theater record and respective seat records in seat table in db
def updateTheater(theaternumber, theaterid):
    data = []
    try:
        with psycopg2.connect(**params) as conn:

            with conn.cursor(cursor_factory = psycopg2.extras.RealDictCursor) as cur:
                query = f'''UPDATE theater SET theaternumber = %s WHERE theaterid = %S RETURNING theaterid;'''
                cur.execute(query, (theaternumber, theaterid))

                data = cur.fetchall()
                data.append({"error":"Record not updated"})
                data.append({"error details": "Theater record not updated"})
                
    except (Exception, psycopg2.DatabaseError) as error:
        data.append({"error":"Error in updateTheater()"})
        data.append({"error details": str(error)})
    finally:
        if conn is not None:
            conn.close()
            return data

#retuns all theater and their showtime, movies for the given mulitplex
def getTheaterInfo(multiplexid):
    data = []
    try:
        with psycopg2.connect(**params) as conn:

            with conn.cursor(cursor_factory = psycopg2.extras.RealDictCursor) as cur:
                query = f'''SELECT theater.theaterid,noofseats, multiplexid, theaternumber, sm.*  from theater
                            INNER JOIN(
                                SELECT showingmaster.theaterid, STRING_AGG(distinct showingmaster.movieid::text, ', ' ORDER BY showingmaster.movieid::text) AS mmovieid,
                                STRING_AGG(distinct m1.moviename, ', ' ) AS mmovienames,STRING_AGG(distinct showtimes::text, ', ') AS mshowtimes
                                FROM showingmaster
                                INNER JOIN (
                                    SELECT moviename, movie.movieid FROM movie
                                )m1 
                                on m1.movieid =showingmaster.movieid
                                GROUP BY showingmaster.theaterid
                            )sm

                            ON sm.theaterid = theater.theaterid
                            where multiplexid = 1;
                            '''
                
                cur.execute(query, (multiplexid, ))

                data = cur.fetchall()
                if len(data) ==0:
                    data.append({"error":"No record found"})
                    data.append({"error details": "No theaters for the selected multiplex!"})
    except (Exception, psycopg2.DatabaseError) as error:
        data.append({"error":"Error in getTheaterInfo()"})
        data.append({"error details": str(error)})
    finally:
        if conn is not None:
            conn.close()
            data = json.dumps(data, indent=4, sort_keys=True, default=str) # to deal with date not being JSON serializable
            data = json.loads(data)
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
                query = "select bookingid, num_seats_booked,totalcost,servicefee,showdate,showtime,price,moviename,runtimeminutes from (select * from (select * from booking inner join showingdetails on booking.showingdetailid = showingdetails.showingdetailid where userid = %s and showingdetails.showdate < CURRENT_DATE) inner join showingmaster using (showingid)) inner join movie using (movieid);"
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
                query = "select bookingid, num_seats_booked,totalcost,servicefee,showdate,showtime,price,moviename,runtimeminutes from (select * from (select * from booking inner join showingdetails on booking.showingdetailid = showingdetails.showingdetailid where userid = %s and showingdetails.showdate > CURRENT_DATE) inner join showingmaster using (showingid)) inner join movie using (movieid);"
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
                query = "select moviename from (select * from (select * from booking inner join showingdetails on booking.showingdetailid = showingdetails.showingdetailid where userid = %s and showingdetails.showdate < CURRENT_DATE) inner join showingmaster using (showingid)) inner join movie using (movieid) where showdate >= CURRENT_DATE - 30;"
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
    


