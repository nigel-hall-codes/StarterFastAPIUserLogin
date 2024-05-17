import psycopg2
from psycopg2 import sql
import configparser

config = configparser.ConfigParser()
config.read("settings.cfg")

# Connect to your PostgreSQL database
conn = psycopg2.connect(
    user=config["Postgres"]["user"],
    password=config["Postgres"]["password"],
    host=config["Postgres"]["host"],
    database=config["Postgres"]["database"],
    port=5432
)

# Create a cursor object using the cursor() method
cursor = conn.cursor()

# Define SQL statements to create tables
create_user_table = sql.SQL("""
    CREATE TABLE IF NOT EXISTS "user" (
    id SERIAL PRIMARY KEY,
    username VARCHAR(50) NOT NULL,
    password_hash VARCHAR NOT NULL,
    created TIMESTAMP,
    email VARCHAR NOT NULL,
    profile_image_s3_path VARCHAR,
    bio TEXT,
    last_login TIMESTAMP,
    is_active BOOLEAN DEFAULT TRUE,
    is_admin BOOLEAN DEFAULT FALSE,
    date_of_birth DATE,
    phone_number VARCHAR
);
""")

def verify_or_create_tables():

    # Execute SQL commands
    cursor.execute(create_user_table)

    # Commit your changes
    conn.commit()

    # Close the cursor and connection
    cursor.close()
    conn.close()


if __name__ == '__main__':
    verify_or_create_tables()
