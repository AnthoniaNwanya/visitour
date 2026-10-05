# VisiTour — Agency Service

The **Agency Service** is a FastAPI microservice for the VisiTour travel platform. It handles agency registration, CAC verification, authentication, profile management, and agency discovery.

## Tech Stack

* Python
* FastAPI
* PostgreSQL
* psycopg2
* JWT Authentication
* Argon2
* Korapay Identity API
* Docker
* AWS

## Project Structure

```text
agency_service/
├── run.py
├── README.md
├── .env
├── .env.example
├── requirements.txt
└── src/
    ├── api/
    │   ├── controllers/
    │   ├── dependencies/
    │   └── routers/
    ├── models/
    ├── repository/
    ├── schemas/
    └── services/
```

## Features

* Agency registration and authentication
* CAC business verification
* JWT Bearer authentication
* Agency profile management
* Agency search and filtering
* Soft deletion
* PostgreSQL persistence

## Setup

Clone the repository:

```bash
git clone git@github.com:AnthoniaNwanya/visitour.git
cd visitour/agency_service
```

Create the virtual environment:

```bash
python3 -m venv .venv
```

Install dependencies:

```bash
.venv/bin/pip install -r requirements.txt
```

Create `.env` from `.env.example` and configure:

```env
DATABASE_HOST=
DATABASE_PORT=5432
DATABASE_NAME=
DATABASE_USER=
DATABASE_PASSWORD=
AUTH_SECRET_KEY=
KORAPAY_SECRET_KEY=
```

Run the service:

```bash
python run.py
```

`run.py` automatically uses the project's `.venv`, so the virtual environment does not need to be activated manually.




## API Documentation

Swagger:

```text
http://127.0.0.1:8000/docs
```

ReDoc:

```text
http://127.0.0.1:8000/redoc
```

## Authentication

Protected endpoints require:

```text
Authorization: Bearer <access_token>
```

## Status

🚧 **Under development**

The Agency Service is the first service in the VisiTour platform. Future services will include Traveler, Travel, and Booking.
