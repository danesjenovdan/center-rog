import os
import re

import psycopg2


def get_alphanum_from_string(input_string):
    result = ""
    for x in input_string:
        if x in ["qwertyuiopasdfghjklzxcvbnmQWERTYUIOPASDFGHJKLZXCVBNM1234567890"]:
            result += x

    return result


# wagtail database connection parameters
host = os.getenv("ROG_DATABASE_HOST", "db")
database = os.getenv("ROG_DATABASE_NAME", "wagtail")
user = os.getenv("ROG_DATABASE_USER", "wagtail")
password = os.getenv("ROG_DATABASE_PASSWORD", "changeme")

# Establish the connection
connection = psycopg2.connect(
    host=host, database=database, user=user, password=password
)

# Create a cursor object
cursor = connection.cursor()

# Define your query
query = """
    SELECT first_name, last_name, uuid
    FROM public.users_user;
"""

# Execute the query
cursor.execute(query)

# Fetch the results
results = cursor.fetchall()

cursor.close()
connection.close()

# consul database connection parameters
host = os.getenv("CONSUL_DATABASE_HOST", "db")
database = os.getenv("CONSUL_DATABASE_NAME", "wagtail")
user = os.getenv("CONSUL_DATABASE_USER", "wagtail")
password = os.getenv("CONSUL_DATABASE_PASSWORD", "changeme")

# Establish the connection
connection = psycopg2.connect(
    host=host, database=database, user=user, password=password
)

# Create a cursor object
cursor = connection.cursor()

existing_users_query = "SELECT document_number FROM public.users;"
cursor.execute(existing_users_query)
existing_users = cursor.fetchall()

rog = set([r[2] for r in results])
consul = set([r[0] for r in existing_users])

difference = rog.difference(consul)

if difference:
    for row in results:
        username = f"{get_alphanum_from_string(row[0])}_{get_alphanum_from_string(row[1])}_{row[2].split('-')[0]}"
        document_number = row[2]
        # Define your query
        query = f"""
            INSERT INTO public.users (
                created_at,
                updated_at,
                confirmed_at,
                username,
                document_number,
                email
            )
            VALUES (
                NOW(),
                NOW(),
                NOW(),
                '{username}',
                '{document_number}',
                '{document_number}'
            )
        """

        # Execute the query
        try:
            cursor.execute(query)
        except psycopg2.errors.UniqueViolation:
            print(f"Unique key violation, rolling back")
            connection.rollback()
else:
    print("No new users.")

connection.commit()
cursor.close()
connection.close()
