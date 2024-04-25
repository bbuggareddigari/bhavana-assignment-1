from pyspark.sql import SparkSession
spark = SparkSession.builder \
    .appName("MySQL Integration") \
    .config("spark.jars", "/path/to/mysql-connector-java-8.0.x.jar") \
    .getOrCreate()
df_employees = spark.read \
    .format("jdbc") \
    .option("url", "jdbc:mysql://localhost:3306/employees") \
    .option("dbtable", "employees") \
    .option("user", "username") \
    .option("password", "password") \
    .load()
print(df_employees.count())
df_employees.printSchema()
df_salaries = spark.read \
    .format("jdbc") \
    .option("url", "jdbc:mysql://localhost:3306/employees") \
    .option("dbtable", "(SELECT * FROM salaries ORDER BY salary DESC LIMIT 10000) as salaries") \
    .option("user", "username") \
    .option("password", "password") \
    .load()
df_salaries.write \
    .format("jdbc") \
    .option("url", "jdbc:mysql://localhost:3306/employees") \
    .option("dbtable", "aces") \
    .option("user", "username") \
    .option("password", "password") \
    .mode("append") \
    .save()
df_salaries.write.option("compression", "snappy").csv("/path/to/save/salaries.csv")
