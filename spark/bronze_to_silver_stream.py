from pyspark.sql import SparkSession
from pyspark.sql.functions import (
    col,
    from_unixtime,
    to_timestamp
)
from pyspark.sql.types import *

spark = (
    SparkSession.builder
    .appName("BronzeToSilverStream")
    .config(
        "spark.sql.extensions",
        "io.delta.sql.DeltaSparkSessionExtension"
    )
    .config(
        "spark.sql.catalog.spark_catalog",
        "org.apache.spark.sql.delta.catalog.DeltaCatalog"
    )
    .master("spark://spark-master:7077")
    .getOrCreate()
)

schema = StructType([
    StructField("symbol", StringType(), True),
    StructField("token", StringType(), True),
    StructField("price", DoubleType(), True),
    StructField("exchange_timestamp", LongType(), True),
    StructField("ingestion_timestamp", StringType(), True),
    StructField("exchange", StringType(), True)
])

bronze_df = (
    spark.readStream
    .format("delta")
    .load("/opt/spark/project/data_delta/bronze/market_ticks")
)

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
        ["token", "exchange_timestamp"]
    )
)

query = (
    silver_df.writeStream
    .format("delta")
    .option(
        "path",
        "/opt/spark/project/data_delta/silver/market_ticks"
    )
    .option(
        "checkpointLocation",
        "/opt/spark/project/checkpoints/silver_stream"
    )
    .outputMode("append")
    .start()
)

query.awaitTermination()