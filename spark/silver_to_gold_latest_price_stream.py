from pyspark.sql import SparkSession
from delta.tables import DeltaTable

spark = (
    SparkSession.builder
    .appName("GoldLatestPriceStream")
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

silver_df = (
    spark.readStream
    .format("delta")
    .load("/opt/spark/project/data_delta/silver/market_ticks")
)

TARGET_PATH = "/opt/spark/project/data_delta/gold/latest_prices"


def upsert_latest(batch_df, batch_id):

    latest_batch = (
        batch_df
        .select(
            "symbol",
            "price",
            "market_time",
            "exchange_timestamp"
        )
    )

    if not DeltaTable.isDeltaTable(spark, TARGET_PATH):

        latest_batch.write \
            .format("delta") \
            .mode("overwrite") \
            .save(TARGET_PATH)

    else:

        target = DeltaTable.forPath(
            spark,
            TARGET_PATH
        )

        (
            target.alias("t")
            .merge(
                latest_batch.alias("s"),
                "t.symbol = s.symbol"
            )
            .whenMatchedUpdate(
                condition="""
                    s.exchange_timestamp >
                    t.exchange_timestamp
                """,
                set={
                    "price": "s.price",
                    "market_time": "s.market_time",
                    "exchange_timestamp":
                        "s.exchange_timestamp"
                }
            )
            .whenNotMatchedInsertAll()
            .execute()
        )


query = (
    silver_df.writeStream
    .foreachBatch(upsert_latest)
    .option(
        "checkpointLocation",
        "/opt/spark/project/checkpoints/gold_latest_price"
    )
    .start()
)

query.awaitTermination()