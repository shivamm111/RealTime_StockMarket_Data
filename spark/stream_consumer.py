from pyspark.sql import SparkSession

spark = (
    SparkSession.builder
    .appName("KafkaMarketData")
    .master("spark://spark-master:7077")
    .config("spark.driver.host", "spark-master")
    .config("spark.driver.bindAddress", "0.0.0.0")
    .getOrCreate()
)
print("✅ Spark Session Created Successfully")

spark.stop()