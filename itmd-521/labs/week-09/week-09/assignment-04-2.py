from pyspark.sql.functions import lit, when, col
from datetime import datetime
df_titles = spark.read \
    .format("jdbc") \
    .option("url", "jdbc:mysql://localhost:3306/employees") \
    .option("query", "SELECT * FROM titles WHERE title = 'Senior Engineer'") \
    .option("user", "username") \
    .option("password", "password") \
    .load()


df_titles = df_titles.withColumn("status", when(col("to_date") == "9999-01-01", "current").otherwise("left"))
df_titles.createOrReplaceTempView("senior_engineers")
df_titles.write \
    .format("jdbc") \
    .option("url", "jdbc:mysql://localhost:3306/employees") \
    .option("dbtable", "left_table") \
    .option("user", "username") \
    .option("password", "password") \
    .mode("errorifexists") 