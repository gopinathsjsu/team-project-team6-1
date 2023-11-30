#API Documentation

<details>

<summary> Release seats</summary>

URL format: POST
/removeMovie

Request format:

```yaml
{
    "bookingid": 1
}
```


```yaml
[
    {
        "seatdetailid": 1
    },
    {
        "seatdetailid": 5
    },
    {
        "seatdetailid": 6
    },
    [
        {
            "showingdetailid": 1
        }
    ]
]
```

</details>


<details>

<summary> Delete showtime</summary>

URL format: POST
/removeMovie

Request format:

```yaml
{
    "showingid": 22,
    "showtime": "17:00:00"
}
```


```yaml
[   ]
```

</details>


<details>

<summary> Delete movie from showing </summary>

URL format: POST
/removeMovie

Request format:

```yaml
{
    "showingid": 1
}
```


```yaml
[   ]
```

</details>

<details>

<summary> Delete theater details from multiplex </summary>

URL format: POST
/removeTheater

Request format:

```yaml
{
    "theaterid": 1
}
```


```yaml
[   ]
```

</details>

<details>

<summary> Fetch theater details from multiplex </summary>

URL format: POST
/getalltheaters

Request format:

```yaml
{
    "multiplexid": 1
}
```

Response format: Response truncated to two records only 

```yaml
[
    {
        "mmovieid": "1, 2, 3",
        "mmovienames": "Creator, Killers Of The Flower Moon, Paw Patrol",
        "mshowtimes": "{10:00:00,12:00:00}, {15:00:00,17:00:00}, {}",
        "multiplexid": 1,
        "noofseats": 10,
        "theaterid": 1,
        "theaternumber": 1
    },
    {
        "mmovieid": "1, 3",
        "mmovienames": "Creator, Killers Of The Flower Moon",
        "mshowtimes": null,
        "multiplexid": 1,
        "noofseats": 10,
        "theaterid": 2,
        "theaternumber": 2
    }
]
```

</details>


<details>

<summary> Add/Update new movie to db </summary>

URL format: POST
/addMovie

Request format:

```yaml
{
    "movieid": 6,//provide this only for update, else do not send this
    "moviename": "Utah",
    "runtimeminutes": "66",
    "releasedate": "2024-10-13",
    "endshowingdate": "2024-12-13",
    "poster": "utah.jpg"
}
```

Response format: Response truncated to two records only 

```yaml
[
    {
        "movieid": 6
    }
]
```

</details>

<details>

<summary> Add/Update new theater to db </summary>

URL format: POST
/addTheater

Request format:

```yaml
{
    "theaterid": 55,//provide this only for update, else do not send this
    "showingid": "29,29,30,30",//provide this only for update, else do not send this
    "multiplexid": 7,
    "noofseats": 20,
    "theaternumber": 6,
    "noofrows": 4,
    "noofcolumns": 5,
    "movieid": "1, 1, 3, 3",
    "price": "12.00, 12.00, 12.25, 12.25",
    "showtimes": "10:00:00, 12:00:00, 15:00:00, 17:00:00"
}
```

Response format: Response truncated to two records only 

```yaml

[
    {
        "theaterid": 17
    }
]

```

</details>

<details>

<summary> Add/Update new multiplex to db </summary>

URL format: POST
/addMultiplex

Request format:

```yaml
{
    "multiplexid": 7,//provide this only for update, else do not send this
    "multiplexname": "AMC Saratoga",
    "locationid": 3,
    "address": "Utah",
    "nooftheaters": 5
}
```

Response format: Response truncated to two records only 

```yaml
[
    {
        "multiplexid": 7
    }
]
```

</details>

<details>

<summary> Add/Update new location to db </summary>

URL format: POST
/addLocation

Request format:

```yaml
{
    "locationid": 3,//provide this only for update, else do not send this
    "city":"San Jose",
    "postalcode": 95126,
    "noofmultiplex": 3
}
```

Response format: Response truncated to two records only 

```yaml
[
    {
        "locationid": 3
    }
]
```

</details>

<details>

<summary> Add/Update new movie to db </summary>

URL format: POST
/addMovie

Request format:

```yaml
{
    "movieid": 6,//provide this only for update, else do not send this
    "moviename": "Utah",
    "runtimeminutes": "66",
    "releasedate": "2024-10-13",
    "endshowingdate": "2024-12-13",
    "poster": "utah.jpg"
}
```

Response format: Response truncated to two records only 

```yaml
[
    {
        "movieid": 6
    }
]
```

</details>

<details>

<summary> Save all info for booking API </summary>

URL format: POST
/saveBooking

Request format:

```yaml
{
    "card_number": "",
    "cvv": "",
    "exp": "",
    "email": "freddy1@gmail.com",
    "rewardpointsused": 0,
    "userdetails": "{'userid': 1, 'card_num': 7788, 'email': 'freddy1@gmail.com', 'membership': True, 'rewards': 10}",
    "moviedetails": "{'moviename': 'Paw Patrol', 'multiplex': 'AMC SARATOGA', 'theater': 3, 'bookingid': '1', 'showdate': '2023-12-13', 'showtime': '19:00:00', 'showingdetailid': 1, 'noofseats': 3, 'seats': [3]}",
    "payment": "{'price': 37.5, 'discount': 0.0, 'tax': 1.88, 'fee': 2.5, 'total': 41.88}"
}
```

Response format: Response truncated to two records only 

```yaml
[
    [
    {
        "seatdetailid": 4
    },
    {
        "bookingid": 1,
        "num_seats_booked": 3,
        "showingdetailid": 1
    },
    {
        "seatsavailable": -4,
        "seatstaken": 24
    },
    {
        "showingdetailid": 1
    }
]
]
```

</details>

<details>

<summary> Fetch BOOKING details API </summary>

URL format: POST
/getBookingDetails

Request format:

```yaml
{
    "bookingid":1
}
```

Response format: Response truncated to two records only 

```yaml
[
    {
        "array_length": 1,
        "discount": "$0.00",
        "price": "$2.50",
        "showdate": "2023-12-13",
        "showingdetailid": 1,
        "showingid": 1,
        "showtime": "19:00:00"
    }
]
```

</details>

<details>

<summary> Fetch card details API </summary>

URL format: POST
/getCardDetails

Request format:

```yaml
{
    "userid": 1
}
```

Response format: Response truncated to two records only 

```yaml

```

</details>


<details>

<summary> Create Booking API </summary>

URL format: POST
/createbooking

Request format:

```yaml
{
    "seatid": [2],
    "showingdetailid":1,
    "userid":1
}
```

Response format: Response truncated to two records only 

```yaml
[
    {
        "bookingid": 5
    }
]
```

</details>


<details>

<summary> Seat Allocation API </summary>

URL format: POST
/getseatmatrix

Request format:

```yaml
{
    "theaterid":1,
    "showdetailid":2
}
```

Response format: Response truncated to two records only 

```yaml
[
    {
        "istaken": false,
        "noofcolumns": 5,
        "noofrows": 2,
        "rownum": 1,
        "seatdetailid": 11,
        "seatid": 1,
        "seatno": 1,
        "showingdetailid": 2,
        "theaterid": 1
    },
    {
        "istaken": false,
        "noofcolumns": 5,
        "noofrows": 2,
        "rownum": 1,
        "seatdetailid": 12,
        "seatid": 2,
        "seatno": 5,
        "showingdetailid": 2,
        "theaterid": 1
    }
]
```

</details>


<details>

<summary> Get Movie Theaters API </summary>

URL format:
/getmovietheaters

Request format: POST

```yaml
{
    "movieid": 1,
    "multiplexid": 1,
    "chosenDate" : "2023-12-13"
}
```

Response format: 

```yaml
[
    {
        "discounts": "$0.00, $0.75",
        "movieid": 1,
        "moviename": "Killers Of The Flower Moon",
        "mshowtimes": "14:00:00, 19:00:00",
        "multiplexid": 1,
        "multiplexname": "ABC multiplex",
        "poster": "KillersOfTheFlowerMoon.jpeg",
        "price": "$2.50",
        "showingid": 1,
        "showingdetailids": "1, 2",
        "theaterid": 1,
        "theaternumber": 1
    }
]
```

</details>

<details>

<summary> Get Multiplex list API </summary>

URL format: GET
/multiplexlist

Request format:

{
    "locationid": 1
}
OR
{}

Response format: Response truncated to two records only 

```yaml
[
    {
        "multiplexid": 1,
        "multiplexname": "ABC multiplex"
    },
    {
        "multiplexid": 2,
        "multiplexname": "DEF multiplex"
    }
]
```

</details>

<details>

<summary> Get Upcoming Movies API </summary>

URL format: GET
/upcomingmovies

Request format:

Response format: 

```yaml
[
    {
        "movieid": 5,
        "moviename": "Tenet",
        "poster": "Tenet.jpg",
        "runtimeminutes": 202
    }
]
```

</details>

<details>

<summary> Get Current movies API </summary>

URL format: GET
/currentmovies

Request format:

Response format: Response truncated to two records only 

```yaml
[
    {
        "movieid": 1,
        "moviename": "Killers Of The Flower Moon",
        "poster": "KillersOfTheFlowerMoon.jpeg",
        "runtimeminutes": 123
    },
    {
        "movieid": 2,
        "moviename": "Paw Patrol",
        "poster": "PawPatrol.jpeg",
        "runtimeminutes": 187
    }
]
```

</details>


<details>

<summary> Login API </summary>

URL format: POST
/signin

Request format:

```yaml
{
    "username": "freddy1@gmail.com",
    "password": "fred1"
}
```

Response format: 

```yaml
[
    {
        "ispremium": true,
        "membershipid": 1,
        "membershiptilldate": "Sun, 13 Oct 2024 00:00:00 GMT",
        "membershiptype": "Premium",
        "rewardpoints": 10,
        "userid": 1,
        "username": "freddy1@gmail.com"
    }
]
```

</details>
