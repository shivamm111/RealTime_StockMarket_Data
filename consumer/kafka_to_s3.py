import os
import time

from kafka import KafkaConsumer

from consumer.parquet_writer import write_parquet
from consumer.uploader import upload_file
from consumer.utils import generate_s3_key

from config.pipeline_config import (
    TOPIC,
    BOOTSTRAP_SERVERS,
    BATCH_SIZE,
    FLUSH_INTERVAL
)

import json


consumer = KafkaConsumer(
    TOPIC,
    bootstrap_servers=BOOTSTRAP_SERVERS,
    value_deserializer=lambda x: json.loads(x.decode("utf-8")),
    auto_offset_reset="latest",
    enable_auto_commit=True
)

print("=" * 60)
print("Kafka → S3 Consumer Started")
print("=" * 60)

buffer = []

last_upload_time = time.time()


def flush_buffer():

    global buffer
    global last_upload_time

    if len(buffer) == 0:
        return

    print(f"\nUploading {len(buffer)} records...")

    parquet_file = write_parquet(buffer)

    upload_file(
        parquet_file,
        generate_s3_key()
    )

    os.remove(parquet_file)

    print("Upload Complete")

    buffer = []

    last_upload_time = time.time()


try:

    for message in consumer:

        buffer.append(message.value)

        print(
            f"Received : {message.value['symbol']} | "
            f"₹{message.value['price']}"
        )

        if len(buffer) >= BATCH_SIZE:
            flush_buffer()

        elif time.time() - last_upload_time >= FLUSH_INTERVAL:
            flush_buffer()

except KeyboardInterrupt:

    print("\nStopping Consumer...")

    flush_buffer()

    consumer.close()

    print("Consumer Closed")