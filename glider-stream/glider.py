import psycopg2
from ogn.client import AprsClient
from ogn.parser import parse, AprsParseError
import datetime
import csv
import os

# CSV setup
csv_file_path = 'beacons_test_output.csv'
write_header = not os.path.exists(csv_file_path)
csv_file = open(csv_file_path, mode='a', newline='', encoding='utf-8')
csv_writer = csv.writer(csv_file)

# --- PostgreSQL setup ---
conn = psycopg2.connect(
    dbname="mydb",
    user="myuser",
    password="password",
    host="localhost",  # or your DB host
    port="5432"        # default PostgreSQL port
)
cursor = conn.cursor()

cursor.execute('''
CREATE TABLE IF NOT EXISTS beacons (
    id SERIAL PRIMARY KEY,
    raw_message TEXT,
    reference_timestamp TEXT,
    aprs_type TEXT,
    beacon_type TEXT,
    name TEXT,
    receiver_name TEXT,
    latitude DOUBLE PRECISION NOT NULL,
    longitude DOUBLE PRECISION NOT NULL,
    timestamp TEXT,
    track DOUBLE PRECISION,
    ground_speed DOUBLE PRECISION,
    altitude DOUBLE PRECISION,
    address TEXT,
    climb_rate DOUBLE PRECISION,
    flightlevel TEXT,
    user_comment TEXT
)
''')
conn.commit()

if write_header:
    csv_writer.writerow([
        "raw_message", "reference_timestamp", "aprs_type", "beacon_type", "name", "receiver_name",
        "latitude", "longitude", "timestamp", "track", "ground_speed", "altitude", "address",
        "climb_rate", "flightlevel", "user_comment"
    ])

# --- Processing function ---
def process_beacon(raw_message):
    try:
        beacon = parse(raw_message)

        if beacon.get('latitude') is None or beacon.get('longitude') is None:
            print("Missing lat/lon, skipping")
            return

        values = (
            beacon.get('raw_message'),
            beacon.get('reference_timestamp').isoformat() if beacon.get('reference_timestamp') else None,
            beacon.get('aprs_type'),
            beacon.get('beacon_type'),
            beacon.get('name'),
            beacon.get('receiver_name'),
            beacon.get('latitude'),
            beacon.get('longitude'),
            beacon.get('timestamp').isoformat() if beacon.get('timestamp') else None,
            beacon.get('track'),
            beacon.get('ground_speed'),
            beacon.get('altitude'),
            beacon.get('address'),
            beacon.get('climb_rate'),
            beacon.get('flightlevel'),
            beacon.get('user_comment')
        )

        cursor.execute('''
            INSERT INTO beacons (
                raw_message, reference_timestamp, aprs_type, beacon_type, name, receiver_name,
                latitude, longitude, timestamp, track, ground_speed, altitude, address,
                climb_rate, flightlevel, user_comment
            ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        ''', values)
        conn.commit()

        print(f"Inserted beacon: {beacon.get('name')} at lat:{beacon.get('latitude')}, lon:{beacon.get('longitude')}")

    except AprsParseError as e:
        print('Error parsing beacon:', e)
    except Exception as e:
        print('Error processing beacon:', e)

# --- Client setup and run ---
if __name__ == "__main__":
    client = AprsClient(aprs_user='N0CALL')
    client.connect()
    try:
        client.run(callback=process_beacon, autoreconnect=True)
    except KeyboardInterrupt:
        print('\nStop ogn gateway')
        client.disconnect()
        conn.close()
