import psycopg2
import os
import logging

logging.basicConfig(level=logging.INFO)

def db_connection(schema_name=None):  # Add schema_name as an optional argument
    try:

        conn = psycopg2.connect(
            dbname=os.getenv('DB_NAME'),
            user=os.getenv('DB_USER'),
            password=os.getenv('DB_PASSWORD'),
            host=os.getenv('DB_HOST')
        )

        if schema_name:  # Check if a schema name was provided
            with conn.cursor() as cur:
                cur.execute(f'SET search_path TO "{schema_name}"')

        return conn

    except psycopg2.Error as e:
        logging.error("Error connecting to the database: %s", e)  # Use logging for errors
        return None

class emailHandler:
    def __init__(self, schema_name=None):  # Allow schema_name to be passed
        self.conn = db_connection(schema_name)  # Pass schema_name to db_connection
        if self.conn is None:
            logging.error("Failed to establish database connection.")
            raise ConnectionError("Failed to establish database connection.")
        else:
            logging.info("Database connection established successfully.")

    def save_email(self, email, subscribe_date):
        if self.conn is None:
            logging.error("Database connection is not established.")
            raise ConnectionError("Database connection is not established.")

        try:
            with self.conn.cursor() as cursor:  # Use context manager for cursor
                logging.info("Executing query: INSERT INTO subscribers (email, date) VALUES (%s, %s)", (email, subscribe_date.isoformat()))
                cursor.execute("INSERT INTO subscribers (email, date) VALUES (%s, %s)",
                           (email, subscribe_date))
            self.conn.commit()
        except psycopg2.Error as e:
            self.conn.rollback()  # Rollback if error occurs
            logging.error("Error executing SQL query: %s", e)
            raise  # Re-raise the exception so it can be handled elsewhere
        finally:
            if self.conn:
                self.conn.close()       

    def get_subscribers(self):
        if self.conn is None:
            logging.error("Database connection is not established.")
            raise ConnectionError("Database connection is not established.")

        try:
            with self.conn.cursor() as cursor:  # Use context manager for cursor
                logging.info("Executing query: SELECT email FROM subscribers")
                cursor.execute("SELECT email FROM subscribers")
                subscribers = [row[0] for row in cursor.fetchall()]
                return subscribers
        except psycopg2.Error as e:
            self.conn.rollback()  # Rollback if error occurs
            logging.error("Error executing SQL query: %s", e)
            raise  # Re-raise the exception so it can be handled elsewhere
        finally:
            if self.conn:
                self.conn.close()
