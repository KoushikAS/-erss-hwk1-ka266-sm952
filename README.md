# Django Web-App for Ride Sharing App

## Overview

This Django-based web-app is a robust server software solution for a ride-sharing service. It allows users to request, drive for, and join rides, catering to three roles: Ride Owner, Ride Driver, and Ride Sharer. The app is designed to handle multiple rides and users with different roles across various rides.

## Features

### User Roles
- **Ride Owner:** Can request rides, specify details (destination, arrival time, passengers, vehicle type, special requests), and edit requests until confirmed. Views ride status until completion.
- **Ride Driver:** Registers as a driver with personal and vehicle information. Searches for open ride requests, claims, starts, and completes rides.
- **Ride Sharer:** Searches for open ride requests, joins rides, views ride status, and edits participation until the ride is confirmed.

### Core Functionalities
- **Account Creation:** Users can create a new account.
- **Login/Logout:** Account holders can log in and out of the system.
- **Driver Registration:** Users can register as drivers, providing personal and vehicle information.
- **Ride Selection:** Users part of multiple rides can select which ride to manage or view.
- **Ride Requesting:** Users can request rides with detailed specifications.
- **Ride Request Editing (Owner):** Ride owners can edit ride details until the ride is confirmed.
- **Ride Status Viewing:** Both owners and sharers can view the status of their rides.
- **Ride Searching (Driver/Sharer):** Drivers and sharers can search for open ride requests matching their criteria.

## Development Environment

- **Framework:** Django (Python-based).
- **Database:** Postgres (not SQLite).
- **Frontend:** Bootstrap.

## Installation and Running the Game

### Prerequisites
- Docker
  
### Installation
1. Clone the repository to your local machine:

```sh
git clone https://github.com/KoushikAS/Ride_Sharing_App.git
cd Ride_Sharing_App/docker-deploy
```

### Running the Game with Docker
1. Use Docker to build and run the containers for both the backend and frontend services.

```sh
docker-compose up --build
```
   
## Accessing the Application

- Access the game through the frontend service's exposed port. http://127.0.0.1:8000/

## Database Management with pgAdmin

For easier view of DB I have enabled PG Admin to connect and view DB.

- **Access pgAdmin**: Navigate to `http://127.0.0.1:5050/` in your web browser to manage the PostgreSQL database.
- **Login Credentials**: Use the email `568@duke.edu` and the password `root` for access.
- **Connecting to the Database**:
  - Click on "Add New Server" to establish a new database connection.
  - Under the "General tab:
    - Name: any value like `db`.
  - Under the "Connection" tab:
    - Host name/address: `db`
    - Username: `postgres`
    - Password: `postgres`


## Contributions

This project was completed as part of an academic assignment with requirments provided requirments.pdf. Contributions were made solely by Koushik Annareddy Sreenath, Shravan MS, adhering to the project guidelines and requirements set by the course ECE-568 Engineering Robust Server Software 

## License

This project is an academic assignment and is subject to university guidelines on academic integrity and software use.

## Acknowledgments

- Thanks to Brian Rogers and the course staff for providing guidance and support throughout the project.
