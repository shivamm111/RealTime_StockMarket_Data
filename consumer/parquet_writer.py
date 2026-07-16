import os
import uuid
from datetime import datetime

import pandas as pd


TEMP_DIR = "temp"

os.makedirs(TEMP_DIR, exist_ok=True)


def write_parquet(records):
    """
    Convert Kafka records to a Parquet file.

    Parameters
    ----------
    records : list
        List of market tick dictionaries.

    Returns
    -------
    str
        Local parquet file path.
    """

    df = pd.DataFrame(records)

    filename = (
        f"market_ticks_"
        f"{datetime.utcnow().strftime('%Y%m%d_%H%M%S_%f')}_"
        f"{uuid.uuid4().hex[:8]}.parquet"
    )

    filepath = os.path.join(TEMP_DIR, filename)

    df.to_parquet(
        filepath,
        engine="pyarrow",
        index=False
    )

    return filepath