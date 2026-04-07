import psycopg2
import os
from dotenv import load_dotenv

load_dotenv()

conn = psycopg2.connect(os.getenv("DATABASE_URL"))
cur = conn.cursor()

cur.execute("SELECT breed, COUNT(*) FROM dog_requests GROUP BY breed;")
rows = cur.fetchall()
for row in rows:
    print(row)

cur.close()
conn.close()