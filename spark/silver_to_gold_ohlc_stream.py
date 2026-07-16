from pyspark.sql import SparkSession
from pyspark.sql.functions import (
    col,
    window,
    first,
    last,
    max,
    min
)
from pyspark.sql.types import *

spark = (
    SparkSession.builder
    .appName("SilverToGoldOHLCStream")
    .config(
        "spark.sql.extensions",
        "io.delta.sql.DeltaSparkSessionExtension"
    )
    .config(
        "spark.sql.catalog.spark_catalog",
        "org.apache.spark.sql.delta.catalog.DeltaCatalog"
    )
    .getOrCreate()
)

spark.sparkContext.setLogLevel("WARN")

schema = StructType([
    StructField("symbol", StringType(), True),
    StructField("token", StringType(), True),
    StructField("price", DoubleType(), True),
    StructField("exchange_timestamp", LongType(), True),
    StructField("ingestion_timestamp", StringType(), True),
    StructField("exchange", StringType(), True),
    StructField("market_time", TimestampType(), True)
])

silver_df = (
    spark.readStream
    .schema(schema)
    .parquet("/opt/spark/project/data/silver_stream/market_ticks")
)

ohlc_df = (
    silver_df
    .withWatermark("market_time", "2 minutes")
    .groupBy(
        window(col("market_time"), "1 minute"),
        col("symbol")
    )
    .agg(
        first("price").alias("open"),
        max("price").alias("high"),
        min("price").alias("low"),
        last("price").alias("close")
    )
)

query = (
    ohlc_df.writeStream
    .format("delta")
    .outputMode("append")
    .option(
        "checkpointLocation",
        "/opt/spark/project/checkpoints/gold_ohlc_stream"
    )
    .start("/opt/spark/project/data_delta/gold/ohlc_1min")
)

query.awaitTermination()