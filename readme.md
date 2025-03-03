# Globant Data Engineering Coding Challenge

## Description
This project is a solution developed for Globant's Data Engineering Coding Challenge. A REST API has been built to migrate historical data from CSV files to an SQL database, meeting the requirements established in the challenge.

## Contents
- [Globant Data Engineering Coding Challenge](#globant-data-engineering-coding-challenge)
  - [Description](#description)
  - [Contents](#contents)
  - [Technologies Used](#technologies-used)
  - [Project Structure](#project-structure)
  - [Installation and Configuration](#installation-and-configuration)
    - [1. Clone the repository](#1-clone-the-repository)
    - [2. Create and activate a virtual environment](#2-create-and-activate-a-virtual-environment)
    - [3. Install dependencies](#3-install-dependencies)
    - [4. Configure environment variables](#4-configure-environment-variables)
    - [5. Run the API](#5-run-the-api)
  - [API Usage](#api-usage)
  - [Section 1: API](#section-1-api)
    - [Available Endpoints](#available-endpoints)
  - [Section 2: SQL](#section-2-sql)
  - [Bonus Track: Cloud, Testing \& Containers](#bonus-track-cloud-testing--containers)
    - [Cloud Deployment](#cloud-deployment)
    - [Testing](#testing)
    - [Docker](#docker)
  - [Project Images](#project-images)

## Technologies Used
- **Python 3.10.13** (Main programming language)
- **FastAPI** (Framework for the REST API)
- **SQLModel** (ORM for database interaction)
- **SQLite** (Database used for development and testing)
- **PostgreSQL** (Database used in production)
- **Docker** (Containerization)
- **Pytest** (Automated testing)
- **Railway.com** (Cloud deployment platform)

## Project Structure
```plaintext
├── app/
│   ├── main.py        # API entry point
│   ├── routes.py      # API route definitions
│   ├── database.py    # Database configuration
│   ├── models.py      # Database models
│   ├── services.py    # Business logic
│   ├── utils.py       # Helper functions
│   ├── middleware.py  # Error handling
│   ├── constants.py   # Project constants
├── data/              # Input data folder
│   ├── departments/   # Department data
│   ├── employees/     # Employee data
│   ├── jobs/          # Job data
├── tests/             # Automated tests
│   ├── config.py      # Test configuration
│   ├── test_api.py    # API endpoint tests
│   ├── test_crud.py   # CRUD entity tests
├── Dockerfile         # Container configuration
├── docker-compose.yml # Docker Compose configuration
├── requirements.txt   # Project dependencies
├── .env               # Environment variables
├── .env.test          # Environment variables for testing
├── .gitignore         # Ignored files in the repository
├── pytest.ini         # Pytest configuration
├── README.md          # Documentation
```

## Installation and Configuration
### 1. Clone the repository
```bash
 git clone https://github.com/your-user/repository-name.git
 cd repository-name
```
### 2. Create and activate a virtual environment
```bash
 python -m venv .venv
 source .venv\Scripts\activate  # On Linux/Mac: source .venv/bin/activate
```
### 3. Install dependencies
```bash
 python -m pip install -r requirements.txt
```
### 4. Configure environment variables
Create a `.env` file and define the `DATABASE_URL` variable:
```env
DATABASE_URL=sqlite:///db/database.db  # For development and testing
# DATABASE_URL=postgresql://user:password@host:port/dbname  # For production
```
### 5. Run the API
```bash
 python -m fastapi dev app/main.py
```
The API will be available at `http://localhost:8000`.

## API Usage
The interactive documentation is available at:
- Swagger UI: [http://localhost:8000/docs](http://localhost:8000/docs)

## Section 1: API
The API provides endpoints to receive and process CSV files with employee, department, and job data.

### Available Endpoints
- **CSV Upload:**
  - `POST /upload/departments/`
  - `POST /upload/jobs/`
  - `POST /upload/employees/`
- **Data Query:**
  - `GET /employees_per_quarter/` (Employees hired per quarter in 2021)
  - `GET /departments_above_mean/` (Departments with hiring above the 2021 average)

Example of a POST request:
```bash
 curl -X POST "http://localhost:8000/upload/employees/" -F "file=@hired_employees.csv"
```

Example of a GET request:
```bash
 curl -X GET "http://localhost:8000/employees_per_quarter/"
```

## Section 2: SQL
SQL queries have been developed to extract key insights from the database.

1. **Number of employees hired per quarter in 2021**

Expected response:
```json
[
  {"department": "Staff", "job": "Recruiter", "Q1": 3, "Q2": 2, "Q3": 0, "Q4": 0}
]
```

2. **Departments that hired more employees than the average**

Expected response:
```json
[
  {"id": 1, "department": "Engineering", "hired": 150},
  {"id": 2, "department": "Marketing", "hired": 90}
]
```

## Bonus Track: Cloud, Testing & Containers
### Cloud Deployment
The application is deployed and available at the following link:  
🔗 [https://globant-coding-challenge-production.up.railway.app](https://globant-coding-challenge-production.up.railway.app)

It is hosted on **Railway.com**, a platform that allows you to implement and deploy web applications

Two containers were used, as follows:
- One for the REST API
- One for the PostgreSQL database

### Testing
Automated tests have been implemented using `pytest` to validate API functionality.

Run tests:
```bash
 pytest test/test_api.py  # API tests
 pytest test/test_crud.py  # CRUD tests
```

### Docker
To run your application in a Docker container, you can use the docker-compose.yml file.

You must ensure that Docker is installed and running.

To start creating the images and running the containers:
```bash
 docker-compose down -v # Stop the container if it is running
 docker-compose up -d --build # Start the containers defined in docker-compose.yml
```

## Project Images
_Add screenshots or diagrams here_

---
This project was developed following best practices, including modularity, testing, and cloud deployment.

