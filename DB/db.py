import psycopg2
import json
import re


credentials = json.load(open("credentials.json"))
PASSWORD = credentials["password"]
conn = psycopg2.connect(
    host = "localhost",
    database = "to_do_db",
    user = "postgres",
    password = PASSWORD
)

cursor = conn.cursor()





