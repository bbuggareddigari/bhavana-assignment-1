package main.scala.Assignment02
import org.apache.spark.sql.SparkSession
import org.apache.spark.sql.functions._
import org.apache.spark.sql.types._

object Assignment02 {
  def main(args: Array[String]): Unit = {

    val spark = SparkSession.builder()
      .appName("assignment_02")
      .getOrCreate()


    val df = spark.read.json("/home/vagrant/Assignment-02/scala/data/iot_devices.json")


    println("Failing devices with battery levels below a threshold:")
    df.filter(col("battery_level") < 10).show()


    println("Offending countries with high levels of CO2 emissions:")
    df.filter(col("co2_level") > 1000)
      .select("cn")
      .distinct()
      .show()


    println("Min and max values for temperature, battery level, CO2, and humidity:")
    df.agg(min("temp"), max("temp"), min("battery_level"), max("battery_level"),
      min("co2_level"), max("co2_level"), min("humidity"), max("humidity"))
      .show()


    println("Sort and group by average temperature, CO2, humidity, and country:")
    df.groupBy("country")
      .agg(avg("temp").alias("avg_temp"), avg("co2_level").alias("avg_co2"),
        avg("humidity").alias("avg_humidity"))
         .orderBy(desc("avg_temp"), desc("avg_co2"), desc("avg_humidity"))
      .show()


    spark.stop()
  }
}