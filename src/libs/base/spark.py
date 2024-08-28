from pyspark.sql import SparkSession


class SparkMixin:
    spark: SparkSession

    def __init__(self):
        self.spark = (
            SparkSession.builder.master("local[*]")
            .appName("spark-local-demyst")
            .getOrCreate()
        )
