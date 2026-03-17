from pyspark.sql import DataFrame, SparkSession


def load_data(spark: SparkSession, path: str, schema) -> DataFrame:
    return (
        spark.read
        .option("sep", "\t")
        .option("header", True)
        .schema(schema)
        .csv(path)
    )