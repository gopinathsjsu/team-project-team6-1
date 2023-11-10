<details>

<summary> Seat Allocation API </summary>

URL format: POST
http://127.0.0.1:5000/getseatmatrix

Request format: 
{
    "theaterid":1,
    "showdetailid":2
}

Response format: 

Response truncated to two records only 

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

</details>


<details>

<summary> Get Movie Theaters API </summary>

URL format:
http://127.0.0.1:5000/getmovietheaters

Request format: POST
{
    "movieid": 1,
    "multiplexid": 1,
    "chosenDate" : "2023-12-13"
}

Response format: 

</details>

<details>

<summary> Get Multiplex list API </summary>

URL format: GET
http://127.0.0.1:5000/multiplexlist

Request format:

Response format: 

Response truncated to two records only 

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

</details>

<details>

<summary> Get Upcoming Movies API </summary>

URL format: GET
http://127.0.0.1:5000/upcomingmovies

Request format:

Response format: 

[
    {
        "movieid": 5,
        "moviename": "Tenet",
        "poster": "Tenet.jpg",
        "runtimeminutes": 202
    }
]

</details>

<details>

<summary> Get Current movies API </summary>

URL format: GET
http://127.0.0.1:5000/currentmovies

Request format:

Response format: 

Response truncated to two records only 

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

</details>


<details>

<summary> Login API </summary>

URL format: POST
http://127.0.0.1:5000/signin

Request format:

{
    "username": "freddy1@gmail.com",
    "password": "fred1"
}

Response format: 

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

</details>