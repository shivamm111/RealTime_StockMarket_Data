from datetime import datetime, timezone
import uuid


def generate_s3_key():
    """
    Generate a partitioned S3 key.

    Structure:

    bronze/
        market_ticks/
            year=YYYY/
                month=MM/
                    day=DD/
                        hour=HH/
                            market_ticks_timestamp_uuid.parquet
    """

    now = datetime.now(timezone.utc)

    filename = (
        f"market_ticks_"
        f"{now.strftime('%Y%m%d_%H%M%S')}_"
        f"{uuid.uuid4().hex[:8]}.parquet"
    )

    return (
        f"bronze/"
        f"market_ticks/"
        f"year={now.year}/"
        f"month={now.month:02d}/"
        f"day={now.day:02d}/"
        f"hour={now.hour:02d}/"
        f"{filename}"
    )