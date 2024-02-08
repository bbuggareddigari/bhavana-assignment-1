from pyspark.sql import SparkSession
from pyspark.sql.types import StructType, StructField, IntegerType, StringType
from pyspark.sql.functions import col, when, count


spark = SparkSession.builder.appName("Assignment01").getOrCreate()

csv_file_path = "/home/vagrant/jhajek/itmd-521/labs/week-04/scala/data/Divvy_Trips_2015-Q1.csv"


df1 = spark.read.option("header", "true").csv(csv_file_path)
print("DataFrame 1:")
df1.printSchema()
print("Record Count: " + str(df1.count()))


schema = StructType([
    StructField("trip_id", IntegerType(), False),
    StructField("start_time", StringType(), False),

])

df2 = spark.read.schema(schema).option("header", "true").csv(csv_file_path)
print("\nDataFrame 2:")
df2.printSchema()
print("Record Count: " + str(df2.count()))


ddl_schema = "trip_id INT, start_time STRING, ... "

df3 = spark.read.option("header", "true").option("inferSchema", "false").schema(ddl_schema).csv(csv_file_path)
print("\nDataFrame 3:")
df3.printSchema()
print("Record Count: " + str(df3.count()))

df_filtered = df3.select("Gender", "Last Name") \
    .filter(
        (col("Last Name").between("A", "K") & (col("Gender") == "female")) |
        (col("Last Name").between("L", "Z") & (col("Gender") == "male"))
    )

grouped_df = df_filtered.groupBy("station").agg(count("*").alias("Total"))
grouped_df.show(10)


spark.stop()
