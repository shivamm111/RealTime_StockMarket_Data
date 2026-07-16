from pyspark.sql import SparkSession
from pyspark.sql.functions import (
    col,
    from_unixtime,
    to_timestamp
)

spark = (
    SparkSession.builder
    .appName("BronzeToSilver")
    .master("spark://spark-master:7077")
    .getOrCreate()
)

# Read Bronze Data

bronze_df = spark.read.parquet(
    "/opt/spark/project/data/bronze/market_ticks"
)

# Transform

silver_df = (
    bronze_df
    .withColumn(
        "market_time",
        to_timestamp(
            from_unixtime(
                col("exchange_timestamp") / 1000
            )
        )
    )
    .dropDuplicates(
        [
            "token",
            "exchange_timestamp"
        ]
    )
)

# Write Silver

(
    silver_df.write
    .mode("overwrite")
    .parquet(
        "/opt/spark/project/data/silver/market_ticks"
    )
)

print("Silver Layer Created Successfully")