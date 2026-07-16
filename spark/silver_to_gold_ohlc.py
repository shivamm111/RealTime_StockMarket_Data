from pyspark.sql import SparkSession
from pyspark.sql.functions import (
    window,
    first,
    last,
    min,
    max
)

spark = (
    SparkSession.builder
    .appName("OHLC1Minute")
    .master("spark://spark-master:7077")
    .getOrCreate()
)

silver_df = (
    spark.readStream
    .format("delta")
    .load("/opt/spark/project/data_delta/silver/market_ticks")
)

ohlc_df = (
    silver_df
    .groupBy(
        "symbol",
        window("market_time", "1 minute")
    )
    .agg(
        first("price").alias("open"),
        max("price").alias("high"),
        min("price").alias("low"),
        last("price").alias("close")
    )
)

(
    ohlc_df.write
    .mode("overwrite")
    .parquet(
        "/opt/spark/project/data/gold/ohlc_1min"
    )
)

print("OHLC Gold Layer Created Successfully")