Sure, here's the README content without markdown formatting:

---

# FastAPI User Management API

This FastAPI application provides endpoints for user management, including user creation and authentication. It uses PostgreSQL for data storage.

## Prerequisites

- Python 3.7+
- PostgreSQL
- `pip` (Python package installer)

## Installation

1. Clone the repository:

   `git clone <repository_url>`

   `cd <repository_directory>`

2. Set up a virtual environment:

   `python3 -m venv env`

   `source env/bin/activate`

3. Install dependencies:

   `pip install -r requirements.txt`

4. Configure environment variables:

   Create a `.env` file in the root directory of the project and add the following variables:

   ```
   USER_API_SECRET=<your_secret_key>
   ```

5. Create the `settings.cfg` file:

   Create a `settings.cfg` file in the root directory of the project and add your PostgreSQL configuration:

   ```
   [database]
   dbname=<your_database_name>
   user=<your_database_user>
   password=<your_database_password>
   host=<your_database_host>
   port=<your_database_port>
   ```

## Database Setup

1. Start PostgreSQL:

   Make sure your PostgreSQL server is running.

2. Create the database:

   `psql -U <your_database_user> -c "CREATE DATABASE <your_database_name>;"`

3. Create the tables:

   The application will automatically create the necessary tables when it starts.

## Running the Application

1. Start the FastAPI application:

   `uvicorn api.server:app --reload`

   The application will be available at `http://127.0.0.1:8000`.

2. Access API documentation:

   - Swagger UI: `http://127.0.0.1:8000/docs`
   - ReDoc: `http://127.0.0.1:8000/redoc`

## Project Structure

```
.
├── api
│   └── server.py
│   └── token_verification.py
├── models
│   └── users.py
├── rds
│   └── rds.py
├── settings.cfg
├── requirements.txt
└── README.md
```

- `api/server.py`: The main application file where the FastAPI app is defined and run.
- `models/users.py`: Defines the User data model.
- `rds/rds.py`: Handles database interactions.
- `api/token_verification.py`: Contains functions for JWT token verification.
- `settings.cfg`: Configuration file for database settings.
- `requirements.txt`: Lists the Python dependencies.
- `README.md`: This file.

## Usage

Sure, here's the README content starting from the "Usage" section without markdown formatting:

---

## Usage

### Create User

Endpoint: `POST /user/create`

Request Body:

```
{
  "username": "string",
  "password": "string",
  "email": "string",
  "profile_image_s3_path": "string",
  "bio": "string",
  "date_of_birth": "YYYY-MM-DD",
  "phone_number": "string"
}
```

Response:

```
{
  "message": "success"
}
```

### Get Access Token

Endpoint: `POST /token`

Form Data:

- `username`: string
- `password`: string

Response:

```
{
  "access_token": "string",
  "token_type": "bearer"
}
```

## License

This project is licensed under the MIT License.
