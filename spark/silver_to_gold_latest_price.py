from pyspark.sql import SparkSession
from pyspark.sql.functions import max as spark_max
spark = (
    SparkSession.builder
    .appName("LatestPrices")
    .master("spark://spark-master:7077")
    .getOrCreate()
)

silver_df = spark.read.parquet(
    "/opt/spark/project/data/silver/market_ticks"
)

latest_ts = silver_df.groupBy("symbol").agg(
    spark_max("exchange_timestamp").alias("latest_ts")
)

gold_df = (
    silver_df.alias("s")
    .join(
        latest_ts.alias("l"),
        (silver_df.symbol == latest_ts.symbol)
        &
        (
            silver_df.exchange_timestamp
            ==
            latest_ts.latest_ts
        )
    )
    .select(
        "s.symbol",
        "s.price",
        "s.market_time"
    )
)

gold_df.write.mode("overwrite").parquet(
    "/opt/spark/project/data/gold/latest_prices"
)

print("Latest Prices Gold Layer Created")