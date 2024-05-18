import psycopg2
from psycopg2 import sql
import pdb
from models import users


class Client:

    def __init__(self, config):
        self.config = config

    def __enter__(self):
        self.db = psycopg2.connect(user=self.config["Postgres"]["user"],
                                   password=self.config["Postgres"]["password"],
                                   host=self.config["Postgres"]["host"],
                                   database=self.config["Postgres"]["database"],
                                   port=5432)
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        if self.db:
            self.db.close()

    def insert_user(self, user):
        with self.db.cursor() as cursor:
            insert_query = """
                   INSERT INTO "user" (
                       username, email, password_hash, created, profile_image_s3_path, 
                       bio, last_login, is_active, is_admin, date_of_birth, phone_number
                   ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
               """
            cursor.execute(insert_query, (
                user.username,
                user.email,
                user.password_hash,
                user.created,
                user.profile_image_s3_path,
                user.bio,
                user.last_login,
                user.is_active,
                user.is_admin,
                user.date_of_birth,
                user.phone_number
            ))
            self.db.commit()

    def get_user(self, username):
        with self.db.cursor() as cursor:
            select_query = """
                SELECT username, email, password_hash, created, profile_image_s3_path, 
                       bio, last_login, is_active, is_admin, date_of_birth, phone_number
                FROM "user"
                WHERE username = %s
            """
            cursor.execute(select_query, (username,))
            row = cursor.fetchone()
            if row:
                user_data = {
                    "username": row[0],
                    "email": row[1],
                    "password_hash": row[2],
                    "created": row[3],
                    "profile_image_s3_path": row[4],
                    "bio": row[5],
                    "last_login": row[6],
                    "is_active": row[7],
                    "is_admin": row[8],
                    "date_of_birth": row[9],
                    "phone_number": row[10]
                }
                return user_data
            else:
                return None
