from kafka import KafkaConsumer
import json

consumer = KafkaConsumer(
    "market_ticks",
    bootstrap_servers="localhost:29092",
    auto_offset_reset="latest",
    group_id="angel_live_consumer"
)

print("Listening...")

for msg in consumer:
    try:
        data = json.loads(msg.value.decode("utf-8"))
        print(data)
    except Exception:
        print("Invalid message:", msg.value.decode("utf-8"))