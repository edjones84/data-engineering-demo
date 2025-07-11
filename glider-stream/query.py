import psycopg2

conn = psycopg2.connect(
    dbname="mydb",
    user="myuser",
    password="password",
    host="localhost",
    port="5432"
)
cursor = conn.cursor()


if __name__ == "__main__":
    cursor.execute("SELECT count(*) FROM beacons;")
    rows = cursor.fetchall()

    for row in rows:
        print(row)

    cursor.close()
    conn.close()
