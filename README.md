# Team 6 CMPE 202 Project Fall 2023

## Team Members: Aishwarya Shankar, Sai Pranavi Kurapati, Sayali Vinod Bayaskar, Divija Choudhary
---
### Name of Application: MovieAnytime
GitHub Project Repo Link: [https://github.com/gopinathsjsu/team-project-team6-1]    
Project Board Link: [https://github.com/gopinathsjsu/team-project-team6-1/tree/main/Project_Journal/ScrumReport]  
Project Journal Link: [https://github.com/gopinathsjsu/team-project-team6-1/tree/main/Project_Journal]      
Google Sprint Task Sheet Link: [https://github.com/gopinathsjsu/team-project-team6-1/tree/main/Project_Journal/SprintSheetsAndBurndownCharts]


### Tech Stack Used
+ Frontend: HTML, CSS, JavaScript
+ Backend: Python Flask Framework
+ Database: PostgreSQL

Rationale behind tech stack decision: Since we are dealing with structured data for this this application, a relational database made sense to use. Most team members were overall familar with PostgreSQL, so we chose to use that. Team members were also familiar with Python programming, and Flask framework makes it easy to create routes/endpoints so we decided to use this for backend. Our team decided to use HTML, CSS, and JavaScript for the frontend as we had not extensively worked with any frontend frameworks prior to this project, so we decided to keep it simple. 
### Feature Set of MovieAnytime:
+ UI accessible by 3 different roles (members, non-members, and employees)
+ All users can:\
View home/landing page which has information on theater, locations, movie schedule, and upcoming movies\
Register/signup as a regular member\
Book tickets for a movie
+ Registered members can:\
View their profile page\
Upgrade to premium membership\
View their past 30-day movies watched list\
Book up to 8 seats for a movie showing\
Cancel their upcoming movie booking and get a refund\
Accumulate reward points (1 point per dollar spent)\
Premium members don't have to pay online service fee for booking\
+ Theater employees can:\
Add, update, and remove movies, showtimes, and theater assignments in the schedule\
Configure seating capacity for a theater in a multiplex\
View analytics for theater occupancy in the past 30/60/90 days summarized by location and by movies\
Configure discount prices for Tuesday movie showings or showings before 6 PM    


## Diagrams  
### Component Diagram  
![component diagram](./diagrams/component.png)
### Architecture Diagram  
![architecture diagram](./diagrams/architecture.png)
### Deployment Diagram  
We've deployed our application and database on AWS. We have 2 EC2 instances serving as our web servers, and a load balancer configured on top of these 2 instances. Our PostgreSQL database is set up in RDS in an auto-scale group. 
![deployment diagram](./diagrams/deployment.png)





## Contributions  
### Aishwarya Shankar  

- Created UI Wireframes for landing page, booking tickets page, and payment page
- Helped design Postgres database schema and populated it with mock data for some tables
- Performed research on tech stack and got up to speed with Python, Flask, and Postgres
- Was Scrum Master for one sprint
- Backend development contributions using Python/Flask:  
wrote user registration/signup API which also allows them to register and obtain immediate Regular membership  
wrote API for users to upgrade to Premium membership  
wrote API to fetch user's profile information to display on membership page  
wrote API to get user's past movie booking history  
wrote API to get user's upcoming movie bookings  
wrote API to get user's movies watched in the past 30 days  
wrote API for user to cancel their upcoming movie booking and get refund  
wrote some helper APIs to get information relevant to employees like multiplexes by location, all cities in db, and movies played in the past 90 days  
wrote API for employees to get theater occupancy analytics for the last 30, 60, and 90 days summarized by locations  
wrote API for employees to get theater occupancy analytics for the last 30, 60, and 90 days summarized by movies  
wrote api for employees to be able to configure discount prices for Tuesday movie showings or showings before 6 PM  
- Wrote team's XP Core Values Reflection
- Setup team's AWS account
- Worked on setting up PostgreSQL database instance in AWS RDS  
- Worked with Sayali to set up load balancer for servers in AWS
- Helped troubleshoot some issues in AWS deployment of application
- Created component diagram, architecture diagram, and deployment diagram
- Wrote the project README.md file  
- Participated in project presentation/demo

### Sayali Vinod Bayaskar  

- Create UI wireframe diagrams for login page, list of movies, employee dashboard and update theater
- Performed research on tech stack for backend and database Python, Flask, and Postgres
- Design Postgres database schema and added some sample data
- Created user stories
- Was Scrum master for 2 sprints
- Backend development contributions using Python/Flask:
    - Wrote API for Login API
    - Wrote API for current movies for homepage
    - Wrote API for upcoming movies for homepage
    - Wrote API for return multiplex list
    - Implement session variable for login page
    - Wrote API for seat allocation matrix
    - Wrote API for payment page
    - Wrote API for getting user details
    - Wrote API for saving card deatils
    - Wrote API for saving booking details
    - Wrote API for generating transaction number
    - Wrote API for adding, updating and removing location, movie, theater, multiplex and showtimes
    - Wrote API for adding, updating and removing seat, seat details, showing detail and showing master
    - Updated the cancel booking API to release seats 
- Frontend development contributions using HTML/CSS:
    - Worked on homepage
    - Worked on booking page
    - Created payment page
- Integrating front to backed contributions:
    - Integrate payment frontend with api
    - Worked on homepage to bookmovie page integration
    - Booking and payment page integration
- Tested the cycle and worked on bug fixing
- Worked with Aishwarya to setup team's AWS account and to create mock data on PostgreSQL database 
- Set up load balancer for servers in AWS
- Participated in project presentation/demo

### Sai Pranavi Kurapati  

- Created UI wireframes for Registration, Member Profile page, Add/update/remove movies/showtimes/theater assignment in the schedule, Configure discount prices for shows before 6 pm and for Tuesday shows.
- Researched and selected the tech stack for the project.
- Designed the database, created tables, and established connections between them.
- Added mock data to the database.
- Acted as the Scrum master for one sprint, leading Scrum meetings.
  
- Frontend Development:
- Login Page:
    - Design and Implementation: Created a login interface using HTML, CSS, and JavaScript.
    - Booking Movie UI: Location, Date, and Multiplex Selection: Designed and implemented a feature allowing users to select location, date, and multiplex.
    - Dynamic Theater Loading: Dynamically loaded theaters based on the user's selection, providing a streamlined user experience.
- Seat Selection Page:
    - Seat Display: Implemented a page to display available, taken, and selected seats for a specific theater.
    - Booking ID Generation: Created functionality to generate a booking ID after seat selection and passed it as a parameter to the payment page.
- Admin Dashboard:
    - UI Design and Implementation: Designed and implemented an intuitive admin dashboard using HTML, CSS, and JavaScript.
- Theater Management:
    - Load Theaters Functionality: Developed a feature to load all theaters of a selected multiplex on the admin dashboard.
    - Add Theater: Implemented the ability to add a new theater to any multiplex, allowing configuration of showtimes, prices, and movies.
    - Edit Theater: Provided functionality to edit showtimes, prices, and movies running in a theater.
- Movie Management:
    - Add Movie: Implemented a feature to add a new movie to the system.
    - Update Movie: Created functionality to update movie details, such as the end showing date or runtime.
    - Delete Movie: Implemented the ability to delete an existing movie.
- Integration and Testing:
    - Integrated Admin Pages: Integrated all admin pages to ensure a cohesive user experience.
    - Thorough Testing: Conducted comprehensive testing on all modules to identify and address potential issues.
- Mock Data Addition: Added mock data to the RDS instance for testing purposes.
- Deployment: Deployed the application on an EC2 instance, making it accessible for users.


### Divija Choudhary 

- Created UI Wireframes for admin landing page, cancel tickets, and membership page
- Prepared mock data for postgresDB
- Was Scrum Master for one sprint
- Frontend development contributions using Html/CSS:
- Designed common landing page for all types of users
- Given two directives for 
 - all current movies
 - all upcoming movies.
- Designed user registration/signup frontend and added validations to it.
- Designed html page to upgrade membership status and make payment page to fulfill the same
- Integrated API and UI for users to upgrade to Premium membership.
- Integrated user profile details to a common profile page
 - Profile(General)
 - View Past Bookings
 - View Upcoming bookings
 - View movies watched in past 30 days

- Designed module for cancel their upcoming movie booking and get refund.
- Researched for the graphichal implementation of the analytics dashboard
- Designed UI for admin anlytics dashboard
 - summarized by location
 - summarized by movie
- Integrated all the UI components and analyzed whole flow.
- Designed configure discount module for shows before 6 pm and for Tuesday shows
- Researched over the deployment process
- Configured global IP for the connection establishment on the ec2.
- Setup the ec2 instance, made sure to have all the project files on the ec2 instance.
- Handled deployment for whole project






























