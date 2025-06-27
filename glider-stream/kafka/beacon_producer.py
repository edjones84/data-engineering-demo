from ogn.client import AprsClient
from ogn.parser import parse, AprsParseError
from kafka import KafkaProducer
import json

producer = KafkaProducer(
    bootstrap_servers='localhost:19092',
    value_serializer=lambda v: json.dumps(v, default=str).encode('utf-8')
)

def process_beacon(raw_message):
    try:
        beacon = parse(raw_message)

        if beacon.get('latitude') is None or beacon.get('longitude') is None:
            print("Missing lat/lon, skipping")
            return

        producer.send('beacons', beacon)
        print(f"Sent beacon to Kafka: {beacon.get('name')}")

    except AprsParseError as e:
        print('Parse error:', e)
    except Exception as e:
        print('Processing error:', e)

if __name__ == "__main__":
    client = AprsClient(aprs_user='N0CALL')
    client.connect()
    try:
        client.run(callback=process_beacon, autoreconnect=True)
    except KeyboardInterrupt:
        print("Stopping producer...")
        client.disconnect()
