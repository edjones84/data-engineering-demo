from kafka import KafkaConsumer
import psycopg2
import json

# Kafka consumer setup
consumer = KafkaConsumer(
    'beacons',
    bootstrap_servers='localhost:19092',
    value_deserializer=lambda m: json.loads(m.decode('utf-8')),
    auto_offset_reset='earliest',
    enable_auto_commit=True,
    group_id='beacon-consumer-group'
)

# PostgreSQL connection setup
conn = psycopg2.connect(
    dbname="mydb",
    user="myuser",
    password="password",
    host="localhost",  # or your DB host
    port="5432"        # default PostgreSQL port
)
cursor = conn.cursor()

# Create table if it doesn't exist
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

# Consume and insert messages
if __name__ == "__main__":
    for msg in consumer:
        beacon = msg.value
        try:
            values = (
                beacon.get('raw_message'),
                beacon.get('reference_timestamp'),
                beacon.get('aprs_type'),
                beacon.get('beacon_type'),
                beacon.get('name'),
                beacon.get('receiver_name'),
                beacon.get('latitude'),
                beacon.get('longitude'),
                beacon.get('timestamp'),
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

            print(f"Inserted beacon into DB: {beacon.get('name')}")

        except Exception as e:
            print("DB insert error:", e)
