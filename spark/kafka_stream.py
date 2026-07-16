from pyspark.sql import SparkSession
from pyspark.sql.functions import col, from_json
from pyspark.sql.types import *

spark = (
    SparkSession.builder
    .appName("BronzeMarketTicks")
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

raw_df = (
    spark.readStream
    .format("kafka")
    .option("kafka.bootstrap.servers", "kafka:9092")
    .option("subscribe", "market_ticks")
    .option("startingOffsets", "latest")
    .load()
)

parsed_df = (
    raw_df
    .selectExpr("CAST(value AS STRING) as json_data")
    .select(
        from_json(
            col("json_data"),
            schema
        ).alias("data")
    )
    .select("data.*")
)

query = (
    parsed_df.writeStream
    .format("delta")
    .option(
        "path",
        "/opt/spark/project/data_delta/bronze/market_ticks"
    )
    .option(
        "checkpointLocation",
        "/opt/spark/project/checkpoints/market_ticks"
    )
    .outputMode("append")
    .start()
)

query.awaitTermination()