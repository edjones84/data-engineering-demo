from kafka import KafkaConsumer
import sqlite3
import json

consumer = KafkaConsumer(
    'beacons',
    bootstrap_servers='localhost:19092',
    value_deserializer=lambda m: json.loads(m.decode('utf-8')),
    auto_offset_reset='earliest',
    enable_auto_commit=True,
    group_id='beacon-consumer-group'
)

if __name__ == "__main__":
    conn = sqlite3.connect('../../demonstration.db')
    c = conn.cursor()

    c.execute('''
    CREATE TABLE IF NOT EXISTS beacons (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        raw_message TEXT,
        reference_timestamp TEXT,
        aprs_type TEXT,
        beacon_type TEXT,
        name TEXT,
        receiver_name TEXT,
        latitude REAL NOT NULL,
        longitude REAL NOT NULL,
        timestamp TEXT,
        track REAL,
        ground_speed REAL,
        altitude REAL,
        address TEXT,
        climb_rate REAL,
        flightlevel TEXT,
        user_comment TEXT
    )
    ''')
    conn.commit()

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

            c.execute('''
                INSERT INTO beacons (
                    raw_message, reference_timestamp, aprs_type, beacon_type, name, receiver_name,
                    latitude, longitude, timestamp, track, ground_speed, altitude, address,
                    climb_rate, flightlevel, user_comment
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', values)
            conn.commit()

            print(f"Inserted beacon into DB: {beacon.get('name')}")

        except Exception as e:
            print("DB insert error:", e)
