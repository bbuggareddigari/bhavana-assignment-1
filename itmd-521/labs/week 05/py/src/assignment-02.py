from pyspark.sql.functions import weekofyear
from pyspark.sql import functions as F
from pyspark.sql.functions import to_date
from pyspark.sql import SparkSession
from pyspark.sql.functions import month, year, count, col, when
from pyspark.sql.window import Window
from pyspark.sql.types import DateType

spark = SparkSession.builder \
    .appName("assignment_02") \
    .getOrCreate()


df = spark.read.csv("sf-fire-calls.csv", header=True, inferSchema=True)


df = df.withColumn("CallDate", to_date(col("CallDate"), "MM/dd/yyyy"))

print("Different types of fire calls in 2018:")
df.filter(year("CallDate") == 2018).select("CallType").distinct().show(10, False)


print("Months within the year 2018 with the highest number of fire calls:")
df.filter(year("CallDate") == 2018).groupBy(month("CallDate").alias("Month")) \
    .agg(count("*").alias("TotalCalls")) \
    .orderBy(col("TotalCalls").desc()).show(10)


print("Neighborhood in San Francisco with the most fire calls in 2018:")
df.filter((year("CallDate") == 2018) & (col("City") == "SF")) \
    .groupBy("Neighborhood").agg(count("*").alias("TotalCalls")) \
    .orderBy(col("TotalCalls").desc()).show(10)


print("Neighborhoods with the worst response times to fire calls in 2018:")
response_time_df = df.filter(F.year("CallDate") == 2018) \
 .withColumn("ResponseTime", F.col("Delay")) \
    .groupBy("Neighborhood").agg(F.avg("ResponseTime").alias("AvgResponseTime")) \
    .orderBy(F.col("AvgResponseTime").desc())
response_time_df.show(10, False)

week_calls_df = df.filter(F.year("CallDate") == 2018) \
    .groupBy(weekofyear("CallDate").alias("Week")) \
    .count() \
    .orderBy(F.col("count").desc()) \
    .withColumnRenamed("count", "TotalCalls")

week_calls_df.show(10, False)

print("Week in the year 2018 with the most fire calls:")
df.filter(year("CallDate") == 2018) \
    .groupBy(weekofyear("CallDate").alias("WatchDate")) \
    .agg(count("*").alias("TotalCalls")) \
    .orderBy(col("TotalCalls").desc()).show(10)

print("Correlation between neighborhood, zip code, and number of fire calls:")
correlation_df = df.groupBy("Neighborhood", "Zipcode").agg(count("*").alias("TotalCalls")) \
    .orderBy(col("TotalCalls").desc())
correlation_df.show(10)


df.write.parquet("fire_calls_data.parquet", mode="overwrite")


parquet_df = spark.read.parquet("fire_calls_data.parquet")
parquet_df.show(10)


df.createOrReplaceTempView("fire_calls_table")
sql_df = spark.sql("SELECT * FROM fire_calls_table WHERE year(CallDateTS) = 2018")
sql_df.show(10)


spark.stop()
