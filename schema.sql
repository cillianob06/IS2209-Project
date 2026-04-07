cur.execute("""
    CREATE TABLE IF NOT EXISTS dog_requests (
        id SERIAL PRIMARY KEY,
        created_at TIMESTAMP DEFAULT NOW()
    );
""")

conn.commit()

cur.execute("SELECT COUNT(*) FROM dog_requests;")
print("Rows in dog_requests:", cur.fetchone()[0])

cur.close()
conn.close()
print("Table created successfully")
CREATE TABLE IF NOT EXISTS favourites (
    id SERIAL PRIMARY KEY,
    image_url TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT NOW()
);