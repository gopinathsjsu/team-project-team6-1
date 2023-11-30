
import time
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
                                STRING_AGG(showingdetailid::text, ', ' ORDER BY showingdetailid) AS showingdetailids,
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
def createTheater(multiplexid, noofseats, theaternumber, noofrows, noofcolumns, movieid, showtimes, price):
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
    except (Exception, psycopg2.DatabaseError) as error:
        data.append({"error":"Error in createTheater()"})
        data.append({"error details": str(error)})
    finally:
        if conn is not None:
            conn.close()
            return data

def createshowingmaster(movieid, showtimes, price, theaterid, no_seats, seats):
    data = []
    values = []
    try:
        with psycopg2.connect(**params) as conn:

            with conn.cursor(cursor_factory = psycopg2.extras.RealDictCursor) as cur:
                movies = movieid.split(",")
                showtimesarr = showtimes.split(",")
                prices = price.split(",")
                prev = 0
                s = 0

                for i in range(0, len(movies)):
                    if(movies[i] == prev):
                        query= f'''UPDATE showingmaster SET showtimes = array_append(showtimes,%s) WHERE showingid = %s'''
                        cur.execute(query,(showtimesarr[i],s))
                    else:
                        prev = movies[i]
                        query = f'''INSERT INTO showingmaster(theaterid, movieid, price, showtimes)  VALUES (%s, %s, %s, Array [%s]) RETURNING showingid;'''
                        cur.execute(query,(theaterid, movies[i], prices[i], showtimesarr[i]))
                        data = cur.fetchall()
                    if len(data) ==0:
                        data.append({"error":"Record not created"})
                        data.append({"error details": "showingmaster record not created"})
                    else:
                        s = data[0]["showingid"]
                        query = f'''INSERT INTO showingdetails(showingid, showdate, showtime, discount, seatsavailable, seatstaken)
	                                VALUES (%s, %s, %s, %s, %s, %s) RETURNING showingdetailid;'''
                        for j in range(10):
                            cur.execute(query,(s, datetime.date.today()+ datetime.timedelta(j), showtimesarr[i], "$0.00", no_seats, 0))
                            data2 = cur.fetchall()
                            values.append(data2[0]["showingdetailid"])
    except (Exception, psycopg2.DatabaseError) as error:
        data.append({"error":"Error in createshowingmaster()"})
        data.append({"error details": str(error)})
    finally:
        if conn is not None:
            conn.close()
            return data, values

def createSeat(theaterid, num_row, num_col):
    data = []
    seatarr = []
    try:
        with psycopg2.connect(**params) as conn:
            with conn.cursor(cursor_factory = psycopg2.extras.RealDictCursor) as cur:
                for i in range(0, num_row):
                    for j in range(0, num_col):
                        query = f'''INSERT INTO seat(rownum, seatno, theaterid) VALUES (%s, %s, %s) RETURNING seatid;'''
                        cur.execute(query,(i, j, theaterid))
                        data = cur.fetchall()
                        seatarr.append(data[0]["seatid"])
    except (Exception, psycopg2.DatabaseError) as error:
        print(str(error))
        data.append({"error":"Error in createSeat()"})
        data.append({"error details": str(error)})
    finally:
        if conn is not None:
            conn.close()
            return data, seatarr


def createSeatDetails(seats, showingdetailid):
    data = []
    seatarr = []
    print(type(seats))
    print(seats)
    try:
        with psycopg2.connect(**params) as conn:
            with conn.cursor(cursor_factory = psycopg2.extras.RealDictCursor) as cur:
                query = f'''INSERT INTO public.seatdetails(seatid, showingdetailid, istaken) VALUES (%s, %s, false);'''
                values = []
                for i in showingdetailid:
                    for j in seats:
                        values.append(tuple((j,i)))
                cur.executemany(query,values)
    except (Exception, psycopg2.DatabaseError) as error:
        print(str(error))
        data.append({"error":"Error in createSeatDetails()"})
        data.append({"error details": str(error)})
    finally:
        if conn is not None:
            conn.close()
            return data, seatarr


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
                query = f'''UPDATE theater SET theaternumber = %s WHERE theaterid = %s RETURNING theaterid;'''
                
                cur.execute(query, (theaternumber, theaterid))

                data = cur.fetchall()
                if len(data) ==0:
                    data.append({"error":"Record not updated"})
                    data.append({"error details": "Theater record not updated"})
                
    except (Exception, psycopg2.DatabaseError) as error:
        data.append({"error":"Error in updateTheater()"})
        data.append({"error details": str(error)})
    finally:
        if conn is not None:
            conn.close()
            return data

def updateshowingmaster(movieid, showtimes, theaterid, noofseats, showingid):
    data = []
    values = []
    try:
        with psycopg2.connect(**params) as conn:

            with conn.cursor(cursor_factory = psycopg2.extras.RealDictCursor) as cur:
                movies = movieid.split(",")
                showtimesarr = showtimes.split(",")
                showingidarr = showingid.split(",")
                prev = 0
                s = 0

                for i in range(0, len(movies)):
                    if(movies[i] == prev):
                        query= f'''UPDATE showingmaster SET showtimes = array_append(showtimes,%s) WHERE showingid = %s'''
                        cur.execute(query,(showtimesarr[i],s))
                    else:
                        prev = movies[i]
                        query = f'''UPDATE showingmaster SET theaterid =%s, movieid =%s, showtimes = Array [%s] WHERE showingid = %s RETURNING showingid;'''
                        cur.execute(query,(theaterid, movies[i], showtimesarr[i], showingidarr[i]))
                        data = cur.fetchall()
                    if len(data) ==0:
                        data.append({"error":"Record not updated"})
                        data.append({"error details": "showingmaster record not updated"})
                    else:
                        s = data[0]["showingid"]
                        query = f'''SELECT MAX( showdate) FROM showingdetails WHERE showingid = %s'''
                        cur.execute(query,(s,))
                        data1 = cur.fetchall()
                        query = f'''INSERT INTO showingdetails(showingid, showdate, showtime, discount, seatsavailable, seatstaken)
	                                VALUES (%s, %s, %s, %s, %s, %s) RETURNING showingdetailid;'''
                        for j in range(10):
                            cur.execute(query,(s, datetime.date.today()+ datetime.timedelta(j), showtimesarr[i], "$0.00", noofseats, 0))
                            data2 = cur.fetchall()
                            values.append(data2[0]["showingdetailid"])
    except (Exception, psycopg2.DatabaseError) as error:
        print(str(error))
        data.append({"error":"Error in updateshowingmaster()"})
        data.append({"error details": str(error)})
    finally:
        if conn is not None:
            conn.close()
            return data, values

def getseats(theaterid):
    data = []
    seats =[]
    try:
        with psycopg2.connect(**params) as conn:

            with conn.cursor(cursor_factory = psycopg2.extras.RealDictCursor) as cur:
                query = f'''SELECT seatid FROM seat WHERE theaterid =%s;'''
                cur.execute(query, (theaterid,))

                data = cur.fetchall()
                if len(data) ==0:
                    data.append({"error":"No record found"})
                    data.append({"error details": "No seats records for the selected theater!"})
                else:
                    for rec in data:
                        seats.append(rec["seatid"])
    except (Exception, psycopg2.DatabaseError) as error:
        data.append({"error":"Error in getseats()"})
        data.append({"error details": str(error)})
    finally:
        if conn is not None:
            conn.close()
            return data, seats

def deleteTheater(theaterid):
    data=[]
    try:
        with psycopg2.connect(**params) as conn:

            with conn.cursor(cursor_factory = psycopg2.extras.RealDictCursor) as cur:
                query = f'''DELETE FROM theater WHERE theaterid = %s'''
                
                cur.execute(query, (theaterid,))

    except (Exception, psycopg2.DatabaseError) as error:
        data.append({"error":"Error in deleteTheater()"})
        data.append({"error details": str(error)})
    finally:
        if conn is not None:
            conn.close()
            return data

def deleteshowingmaster(theaterid):
    data=[]
    try:
        with psycopg2.connect(**params) as conn:

            with conn.cursor(cursor_factory = psycopg2.extras.RealDictCursor) as cur:
                query = f'''SELECT showingid FROM showingmaster WHERE theaterid = %s'''
                cur.execute(query,(theaterid,))
                data = cur.fetchall()
            
                for rec in data:
                    query = f'' 'DELETE FROM showingdetails WHERE showingid = %s'' '
                    cur.execute(query,(rec["showingid"],))
                query = f'' 'DELETE FROM showingmaster WHERE theaterid = %s'' '
                
                cur.execute(query, (theaterid,))
                

    except (Exception, psycopg2.DatabaseError) as error:
        data.append({"error":"Error in deleteshowingmaster()"})
        data.append({"error details": str(error)})
    finally:
        if conn is not None:
            conn.close()
            return data

def deleteseat(theaterid):
    data=[]
    try:
        with psycopg2.connect(**params) as conn:

            with conn.cursor(cursor_factory = psycopg2.extras.RealDictCursor) as cur:
                query = f'''SELECT seatid FROM seat WHERE theaterid = %s'''
                cur.execute(query,(theaterid,))
                data = cur.fetchall()
            
                for rec in data:
                    query = f'' 'DELETE FROM seatdetails WHERE seatid = %s'' '
                    cur.execute(query,(rec["seatid"],))
                query = f'' 'DELETE FROM seat WHERE theaterid = %s'' '
                
                cur.execute(query, (theaterid,))
    except (Exception, psycopg2.DatabaseError) as error:
        data.append({"error":"Error in deleteseat()"})
        data.append({"error details": str(error)})
    finally:
        if conn is not None:
            conn.close()
            return data

def deleteshowingmaster1(showingid):
    data=[]
    values = []
    try:
        with psycopg2.connect(**params) as conn:

            with conn.cursor(cursor_factory = psycopg2.extras.RealDictCursor) as cur:
                query = f'''SELECT showingdetailid FROM showingdetails WHERE showingid = %s'''
                cur.execute(query,(showingid,))
                data = cur.fetchall()
                for rec in data:
                    values.append(rec["showingdetailid"])
                query = f'''DELETE FROM showingdetails WHERE showingid = %s'''
                cur.execute(query,(showingid,))
                query = f'''DELETE FROM showingmaster WHERE showingid = %s'''
                cur.execute(query, (showingid,))
    except (Exception, psycopg2.DatabaseError) as error:
        print(str(error))
        data.append({"error":"Error in deleteshowingmaster1()"})
        data.append({"error details": str(error)})
    finally:
        if conn is not None:
            conn.close()
            return data, values

def deleteseat1(showingdetailid):
    data=[]
    try:
        with psycopg2.connect(**params) as conn:

            with conn.cursor(cursor_factory = psycopg2.extras.RealDictCursor) as cur:
                query = f'''DELETE FROM seatdetails WHERE showingdetailid = ANY (%s::int[])'''
                cur.execute(query, ("{" + (",".join(map(str, showingdetailid))) + "}",))
    except (Exception, psycopg2.DatabaseError) as error:
        print(str(error))
        data.append({"error":"Error in deleteseat1()"})
        data.append({"error details": str(error)})
    finally:
        if conn is not None:
            conn.close()
            return data
def deleteshowtime(showingid, showtime):
    data=[]
    values =[]
    try:
        with psycopg2.connect(**params) as conn:

            with conn.cursor(cursor_factory = psycopg2.extras.RealDictCursor) as cur:
                query = f'''SELECT ARRAY_REMOVE(showtimes, %s) FROM showingmaster WHERE showingid = %s'''
                cur.execute(query, (showtime, showingid))

                query = f'''SELECT showingdetailid FROM showingdetails WHERE showtime = %s AND showingid = %s AND showdate>CURRENT_DATE'''
                cur.execute(query, (showtime, showingid))
                data = cur.fetchall()
                for rec in data:
                    values.append(rec["showingdetailid"])
                query = f'''DELETE FROM showingdetails WHERE showtime = %s AND showingid = %s AND showdate>CURRENT_DATE'''
                cur.execute(query, (showtime, showingid))

    except (Exception, psycopg2.DatabaseError) as error:
        print(str(error))
        data.append({"error":"Error in deleteshowtime()"})
        data.append({"error details": str(error)})
    finally:
        if conn is not None:
            conn.close()
            return data, values

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
        print("jsonifydata",jsonify(data))
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
    
# function to release seats for user's cancelled movie booking
def releaseSeats(bookingId):
    data = []
    try:
        with psycopg2.connect(**params) as conn:

            with conn.cursor(cursor_factory = psycopg2.extras.RealDictCursor) as cur:
                query = f'''select seatid, showingdetailid from booking where bookingid = %s;'''
                cur.execute(query, (bookingId,))
                
                data = cur.fetchall()
                seats = data[0]["seatid"]
                showingdetailid = data[0]["showingdetailid"]
                query = f'''UPDATE seatdetails SET istaken = false WHERE seatdetailid = ANY (%s::int[]) RETURNING seatdetailid'''
                cur.execute(query, ("{" + (",".join(map(str, seats))) + "}",))
                data = cur.fetchall()
                if len(data) ==0:
                    data.append({"error":"Record found"})
                    data.append({"error details": "Seats could not be released."})
                query = f'''UPDATE showingdetails SET seatsavailable = seatsavailable+%s, seatstaken =seatstaken-%s WHERE showingdetailid = %s RETURNING showingdetailid'''
                cur.execute(query, (len(seats), len(seats), showingdetailid))
                data.append(cur.fetchall())
                if len(data) ==0:
                    data.append({"error":"Record found"})
                    data.append({"error details": "Seats could not be released."})
                
    except (Exception, psycopg2.DatabaseError) as error:
        data.append({"error":"Error in releaseSeats()"})
        data.append({"error details": str(error)})
    finally:
        if conn is not None:
            conn.close()
            print('database connection closed')
        return data
  


# function to cancel user's movie booking
def cancelBooking(bookingId):
    data = []
    try:
        #establish connection
        with psycopg2.connect(**params) as conn:

            # create a cursor 
                cursor = conn.cursor()
                query = "update booking set status='FALSE',refundstatus='TRUE' WHERE bookingid = %s;"
                cursor.execute(query,(bookingId,))
                conn.commit()
                cursor = conn.cursor(cursor_factory = psycopg2.extras.RealDictCursor)
                queryValidate = "select * from booking where bookingid = %s;"
                cursor.execute(queryValidate,(bookingId,))
                data = cursor.fetchone()
                print(data)
                print(data['status'])
                print(data['refundstatus'])
                if data['status'] != False and data['refundstatus'] != True:
                    data.append({"error":"Incorrect record found"})
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
                query = "select distinct city,locationid from location;"
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
    


# function to calculate theater occupancy by specific location over the past 30, 60, and 90 days
def theaterOccupancyByLocation(locationid):
    print("location id in dbconnector",locationid)
    data = []
    try:
        #establish connection
        with psycopg2.connect(**params) as conn:

            # create a cursor 
                cursor = conn.cursor(cursor_factory = psycopg2.extras.RealDictCursor)
                # query30days = "select sum(seatstaken) as totalTaken, sum(noofseats) as totalAvailable from (select locationid,showdate,seatstaken,noofseats from showingdetails inner join (select * from (select * from (location inner join multiplex using (locationid)) inner join theater using (multiplexid)) inner join showingmaster using (theaterid)) using (showingid) group by locationid,showdate,seatstaken,noofseats having locationid=%s and showdate >= CURRENT_DATE-30);"
                query30days="select sum(seatstaken) as totalTaken,sum(noofseats) as totalAvailable from (select locationid,showdate,seatstaken,noofseats from showingdetails inner join (select * from (select * from (location inner join multiplex using (locationid)) as subquery_4 inner join theater using (multiplexid)) as subquery_3 inner join showingmaster using (theaterid)) as subquery_2 using (showingid) group by locationid,showdate,seatstaken,noofseats having locationid=%s and showdate >= CURRENT_DATE-30 and showdate<=Current_date) as subquery_1;"
                # print("query30days",query30days)
                cursor.execute(query30days,(locationid,))
                row = cursor.fetchone()
                print("row",row)
                if row['totaltaken'] == None or row['totalavailable'] == None:
                    totalNumSeatsTakenAtLoc30days = 0
                    totalNumSeatsAtLoc30days = 1
                else:
                    totalNumSeatsAtLoc30days = row['totalavailable']
                    totalNumSeatsTakenAtLoc30days = row['totaltaken']

                # query60days = "select sum(seatstaken) as totalTaken, sum(noofseats) as totalAvailable from (select locationid,showdate,seatstaken,noofseats from showingdetails inner join (select * from (select * from (location inner join multiplex using (locationid)) inner join theater using (multiplexid)) inner join showingmaster using (theaterid)) using (showingid) group by locationid,showdate,seatstaken,noofseats having locationid=%s and showdate >= CURRENT_DATE-60);"
                query60days="select sum(seatstaken) as totalTaken,sum(noofseats) as totalAvailable from (select locationid,showdate,seatstaken,noofseats from showingdetails inner join (select * from (select * from (location inner join multiplex using (locationid)) as subquery_4 inner join theater using (multiplexid)) as subquery_3 inner join showingmaster using (theaterid)) as subquery_2 using (showingid) group by locationid,showdate,seatstaken,noofseats having locationid=%s and showdate >= CURRENT_DATE-60 and showdate<=Current_date) as subquery_1;"
                cursor.execute(query60days,(locationid,))
                row = cursor.fetchone()
                if row['totaltaken'] == None or row['totalavailable'] == None:
                    totalNumSeatsTakenAtLoc60days = 0
                    totalNumSeatsAtLoc60days = 1
                else:
                    totalNumSeatsAtLoc60days = row['totalavailable']
                    totalNumSeatsTakenAtLoc60days = row['totaltaken']

                # query90days = "select sum(seatstaken) as totalTaken, sum(noofseats) as totalAvailable from (select locationid,showdate,seatstaken,noofseats from showingdetails inner join (select * from (select * from (location inner join multiplex using (locationid)) inner join theater using (multiplexid)) inner join showingmaster using (theaterid)) using (showingid) group by locationid,showdate,seatstaken,noofseats having locationid=%s and showdate >= CURRENT_DATE-90);"
                query90days="select sum(seatstaken) as totalTaken,sum(noofseats) as totalAvailable from (select locationid,showdate,seatstaken,noofseats from showingdetails inner join (select * from (select * from (location inner join multiplex using (locationid)) as subquery_4 inner join theater using (multiplexid)) as subquery_3 inner join showingmaster using (theaterid)) as subquery_2 using (showingid) group by locationid,showdate,seatstaken,noofseats having locationid=%s and showdate >= CURRENT_DATE-90 and showdate<=Current_date) as subquery_1;"
                cursor.execute(query90days,(locationid,))
                row = cursor.fetchone()
                if row['totaltaken'] == None or row['totalavailable'] == None:
                    totalNumSeatsTakenAtLoc90days = 0
                    totalNumSeatsAtLoc90days = 1
                else:
                    totalNumSeatsAtLoc90days = row['totalavailable']
                    totalNumSeatsTakenAtLoc90days = row['totaltaken']

                
                percentOccupied30days = (totalNumSeatsTakenAtLoc30days/totalNumSeatsAtLoc30days)*100
                percentOccupied30days = round(percentOccupied30days,2)
                percentOccupied60days = (totalNumSeatsTakenAtLoc60days/totalNumSeatsAtLoc60days)*100
                percentOccupied60days = round(percentOccupied60days,2)
                percentOccupied90days = (totalNumSeatsTakenAtLoc90days/totalNumSeatsAtLoc90days)*100
                percentOccupied90days = round(percentOccupied90days,2)

                returnDict = {'No of days':['over30days','over60days','over90days'], 'Occupancy Percentage': [percentOccupied30days, percentOccupied60days, percentOccupied90days]}
                data.append(returnDict)
                print(data)
                if len(data) ==0:
                    data.append({"error":"No record found"})
                    data.append({"error details": "No occupancy found in db"})
    except (Exception, psycopg2.DatabaseError) as error:
        data.append({"error":"Error in retrieving theater occupancy info"})
        data.append({"error details": str(error)})
    finally:
        if conn is not None:
            conn.close()
            print('database connection closed')
        data = json.dumps(data, indent=4, sort_keys=True, default=str) # to deal with date not being JSON serializable
        data = json.loads(data)
        return jsonify(data)


# function to calculate theater occupancy by specific movie over the past 30, 60, and 90 days
def theaterOccupancyByMovie(moviename):
    print("moviename in dbconnector",moviename)
    data = []
    try:
        #establish connection
        with psycopg2.connect(**params) as conn:

            # create a cursor 
                cursor = conn.cursor()
                queryForMovieId = "select movieid from movie where moviename=%s"
                cursor.execute(queryForMovieId,(moviename,))
                movieid = cursor.fetchone()[0]
                cursor = conn.cursor(cursor_factory = psycopg2.extras.RealDictCursor)

                # queryForOccupancyInfo30days = "select sum(seatstaken) as taken, sum(noofseats) as total from (select showdate, seatstaken, theaterid, movieid,noofseats from theater inner join (select * from showingdetails inner join showingmaster using (showingid)) using (theaterid) group by theaterid,movieid,seatstaken,showdate,noofseats having movieid=%s and showdate >= CURRENT_DATE-30 and showdate <= CURRENT_DATE);"
                queryForOccupancyInfo30days="select sum(seatstaken) as taken,sum(noofseats) as total from (select showdate, seatstaken, theaterid, movieid,noofseats from theater inner join (select * from showingdetails inner join showingmaster using (showingid)) as subquery_2 using (theaterid) group by theaterid,movieid,seatstaken,showdate,noofseats having movieid=%s and showdate >= CURRENT_DATE-30 and showdate <= CURRENT_DATE) as subquery_1;"
                cursor.execute(queryForOccupancyInfo30days,(movieid,))
                row = cursor.fetchone()
                print(row)
                if row['taken'] == None or row['total'] == None:
                    totalSeatsTakenAtMovie30days = 0
                    totalSeatsAvailableAtMovie30days = 1
                else:
                    totalSeatsTakenAtMovie30days = row['taken']
                    totalSeatsAvailableAtMovie30days = row['total']

                queryForOccupancyInfo60days="select sum(seatstaken) as taken,sum(noofseats) as total from (select showdate, seatstaken, theaterid, movieid,noofseats from theater inner join (select * from showingdetails inner join showingmaster using (showingid)) as subquery_2 using (theaterid) group by theaterid,movieid,seatstaken,showdate,noofseats having movieid=%s and showdate >= CURRENT_DATE-60 and showdate <= CURRENT_DATE) as subquery_1;"
                cursor.execute(queryForOccupancyInfo60days,(movieid,))
                row = cursor.fetchone()
                print(row)
                if row['taken'] == None or row['total'] == None:
                    totalSeatsTakenAtMovie60days = 0
                    totalSeatsAvailableAtMovie60days = 1
                else:
                    totalSeatsTakenAtMovie60days = row['taken']
                    totalSeatsAvailableAtMovie60days = row['total']

                queryForOccupancyInfo90days="select sum(seatstaken) as taken,sum(noofseats) as total from (select showdate, seatstaken, theaterid, movieid,noofseats from theater inner join (select * from showingdetails inner join showingmaster using (showingid)) as subquery_2 using (theaterid) group by theaterid,movieid,seatstaken,showdate,noofseats having movieid=%s and showdate >= CURRENT_DATE-90 and showdate <= CURRENT_DATE) as subquery_1;"
                cursor.execute(queryForOccupancyInfo90days,(movieid,))
                row = cursor.fetchone()
                print(row)
                if row['taken'] == None or row['total'] == None:
                    totalSeatsTakenAtMovie90days = 0
                    totalSeatsAvailableAtMovie90days = 1
                else:
                    totalSeatsTakenAtMovie90days = row['taken']
                    totalSeatsAvailableAtMovie90days = row['total']

                percentOccupied30days = (totalSeatsTakenAtMovie30days/totalSeatsAvailableAtMovie30days)*100
                percentOccupied30days = round(percentOccupied30days,2)
                percentOccupied60days = (totalSeatsTakenAtMovie60days/totalSeatsAvailableAtMovie60days)*100
                percentOccupied60days = round(percentOccupied60days,2)
                percentOccupied90days = (totalSeatsTakenAtMovie90days/totalSeatsAvailableAtMovie90days)*100
                percentOccupied90days = round(percentOccupied90days,2)

                returnDict = {'No of days':['over30days','over60days','over90days'], 'Occupancy Percentage': [percentOccupied30days, percentOccupied60days, percentOccupied90days]}
                
                data.append(returnDict)
                print(data)
                if len(data) ==0:
                    data.append({"error":"No record found"})
                    data.append({"error details": "No occupancy found in db"})
    except (Exception, psycopg2.DatabaseError) as error:
        data.append({"error":"Error in retrieving theater occupancy info"})
        data.append({"error details": str(error)})
    finally:
        if conn is not None:
            conn.close()
            print('database connection closed')
        data = json.dumps(data, indent=4, sort_keys=True, default=str) # to deal with date not being JSON serializable
        data = json.loads(data)
        return jsonify(data)
    

# function to configure discount prices for a particular movie that's showing on Tuesday or pre-6pm 
def configDiscount(movieid, discount, showdate):
    data = []
    try:
        #establish connection
        with psycopg2.connect(**params) as conn:

            # create a cursor 
                cursor = conn.cursor()
                query = "update showingdetails set discount=%s where showingdetailid in (SELECT showingdetailid FROM showingdetails inner join showingmaster using (showingid) WHERE (extract(DOW FROM showdate) = 2 or showtime<'18:00:00') and showdate=%s and movieid=%s);"
                cursor.execute(query,(discount,showdate,movieid,))
                conn.commit()
                cursor = conn.cursor(cursor_factory = psycopg2.extras.RealDictCursor)
                queryValidate="select * from showingdetails where showingdetailid in (SELECT showingdetailid FROM showingdetails inner join showingmaster using (showingid) WHERE (extract(DOW FROM showdate) = 2 or showtime<'18:00:00') and showdate=%s and movieid=%s);"
                cursor.execute(queryValidate,(showdate, movieid,))
                data = cursor.fetchall()
                print("data in dbconeector",data)
                print(data)
                for row in data:
                    print("row before",row)
                    if row['discount'] != ('$'+ discount):
                        print("row",row)
                        print("discount",row['discount'])
                        data.append({"error":"Error"})
                        data.append({"error details": "Discount price was not updated successfully."})
                        break
                    
    except (Exception, psycopg2.DatabaseError) as error:
        data.append({"error":"Discount price was not updated successfully."})
        data.append({"error details": str(error)})
    finally:
        if conn is not None:
            conn.close()
            print('database connection closed')
        data = json.dumps(data, indent=4, sort_keys=True, default=str) # to deal with date not being JSON serializable
        data = json.loads(data)
        print("before jsonify",data)
        return jsonify(data)