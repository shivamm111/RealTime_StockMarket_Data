from consumer.uploader import upload_json
from consumer.utils import generate_s3_key

sample_data = [
    {
        "symbol": "TCS",
        "price": 4200
    },
    {
        "symbol": "INFY",
        "price": 1625
    }
]


upload_json(
    sample_data,
    generate_s3_key()
)