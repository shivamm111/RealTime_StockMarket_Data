import os

from consumer.parquet_writer import write_parquet
from consumer.uploader import upload_file
from consumer.utils import generate_s3_key


records = [
    {
        "symbol": "TCS",
        "price": 4200
    },
    {
        "symbol": "INFY",
        "price": 1650
    }
]

file_path = write_parquet(records)

upload_file(
    file_path,
    generate_s3_key()
)

os.remove(file_path)

print("Finished")