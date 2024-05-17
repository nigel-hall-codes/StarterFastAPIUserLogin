import psycopg2
from psycopg2 import sql


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
