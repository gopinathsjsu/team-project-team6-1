#API Documentation


<details>

<summary> Fetch card details API </summary>

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
        "rownum": 1,
        "seatdetailid": 11,
        "seatid": 1,
        "seatno": 1,
        "showingdetailid": 2
    },
    {
        "istaken": false,
        "rownum": 1,
        "seatdetailid": 12,
        "seatid": 2,
        "seatno": 5,
        "showingdetailid": 2
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
        "showingids": "1, 1",
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
