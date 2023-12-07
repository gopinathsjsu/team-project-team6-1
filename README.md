# Team 6 CMPE 202 Project Fall 2023

## Team Members: Aishwarya Shankar, Sai Pranavi Kurapati, Sayali Vinod Bayaskar, Divija Choudhary
---
### Name of Application: MovieAnytime
GitHub Project Repo Link: [https://github.com/gopinathsjsu/team-project-team6-1] \
Project Board Link:\
Project Journal Link: https://github.com/gopinathsjsu/team-project-team6-1/tree/main/Project_Journal  
Google Sprint Task Sheet Link:  


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
- Helped troubleshoot some issues in AWS deployment of application
- Created component diagram and architecture diagram
- Worked on project README.md file  

### Sayali Vinod Bayaskar  

### Sai Pranavi Kurapati  

### Divija Choudhary  






























